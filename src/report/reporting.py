"""Ledger-backed report views and XLSX export."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
from uuid import uuid4
from zoneinfo import ZoneInfo
from openpyxl import Workbook
from src.paper.ledger import gross_pnl, net_pnl

TR = ZoneInfo("Europe/Istanbul")
SHEETS = ("İşlem Geçmişi", "PnL Detay", "Karar Detayları", "İndikatör Değerleri", "Config Snapshot", "Hata Logları")

@dataclass(frozen=True)
class ReportFilters:
    start: datetime | None = None
    end: datetime | None = None
    symbol: str | None = None
    direction: str | None = None
    result: str | None = None
    exit_reason: str | None = None

@dataclass(frozen=True)
class ExportLog:
    export_id: str
    exported_at_utc: datetime
    exported_at_tr: datetime
    filter_snapshot: dict
    row_counts: dict
    file_format: str = "xlsx"
    library: str = "openpyxl"
    library_version: str = "3.1.5"
    export_status: str = "PASS"
    blocked_reason: str | None = None

def filter_records(records, filters=ReportFilters()):
    result = []
    for record in records:
        if filters.symbol and getattr(record, "symbol", None) != filters.symbol: continue
        if filters.direction and getattr(record, "direction", None) != filters.direction: continue
        if filters.exit_reason and getattr(record, "exit_reason", None) != filters.exit_reason: continue
        if filters.result and getattr(record, "net_pnl", None) is not None:
            if ("WIN" if record.net_pnl > 0 else "LOSS") != filters.result: continue
        timestamp = getattr(record, "timestamp_utc", None)
        if isinstance(timestamp, datetime) and ((filters.start and timestamp < filters.start) or (filters.end and timestamp > filters.end)): continue
        result.append(record)
    return result

def validate_ledger_consistency(records):
    if not records: return "WARNING", "LEDGER_DATA_MISSING"
    for record in records:
        if getattr(record, "action", None) != "EXIT": continue
        expected_gross = gross_pnl(record.direction, record.entry_price, record.exit_price, record.quantity)
        expected_net = net_pnl(expected_gross, record.taker_fee, record.funding_fee, record.slippage_amount)
        if record.gross_pnl != expected_gross or record.net_pnl != expected_net:
            return "BLOCKING_ERROR", "LEDGER_PNL_MISMATCH"
    return "PASS", None

def build_report(ledger_records, filters=ReportFilters()):
    records = filter_records(ledger_records, filters)
    return {"trade_history": records, "pnl_detail": records, "decision_detail": records,
            "indicator_values": [], "config_snapshot": [getattr(r, "config_snapshot", {}) for r in records], "error_logs": []}

def export_xlsx(ledger_records, path, filters=ReportFilters()):
    report = build_report(ledger_records, filters)
    status, blocked = validate_ledger_consistency(ledger_records)
    keys = dict(zip(SHEETS, ("trade_history", "pnl_detail", "decision_detail", "indicator_values", "config_snapshot", "error_logs")))
    workbook = Workbook()
    workbook.remove(workbook.active)
    for sheet_name in SHEETS:
        sheet = workbook.create_sheet(sheet_name)
        rows = report[keys[sheet_name]]
        data = [asdict(row) if hasattr(row, "__dataclass_fields__") else row for row in rows]
        headers = list(data[0].keys()) if data and isinstance(data[0], dict) else []
        if headers:
            sheet.append(headers)
            for row in data:
                values = []
                for header in headers:
                    value = row.get(header)
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value, ensure_ascii=False)
                    elif isinstance(value, datetime):
                        value = value.isoformat()
                    elif hasattr(value, "as_tuple"):
                        value = float(value)
                    values.append(value)
                sheet.append(values)
        else:
            sheet.append(["Kayıt yok"])
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
    now = datetime.now(timezone.utc)
    return ExportLog(str(uuid4()), now, now.astimezone(TR), asdict(filters), {k: len(v) for k, v in report.items()}, export_status=status, blocked_reason=blocked)
