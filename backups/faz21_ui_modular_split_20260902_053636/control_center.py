"""Reference-aligned, paper-only Control Center state and safe intents."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

TOP_STATUS_FIELDS = ("algorithm", "mode", "market", "data", "engine", "scheduler", "health", "clock")
MARKET_COLUMNS = ("SYMBOL", "PRICE", "Δ %", "VOLUME", "BEHAVIOR / STATE", "DIRECTION", "MOD / SIGNAL", "STATE", "BLOCK REASON", "RANK", "RISK", "FINAL")
STATE_LIFECYCLE = ("SCANNING", "WATCH", "PREP", "CANDIDATE", "READY", "POSITION", "EXITED", "DROPPED")
INTELLIGENCE_FIELDS = ("T3", "T3 color", "DMI +DI / -DI", "ADX", "ADX threshold", "ADX slope", "Signal result", "Final decision", "Block reason")
RISK_FIELDS = ("wallet/equity", "free balance", "allocation", "max coin", "quantity", "min notional", "leverage", "stop loss", "same-symbol lock", "no hedge", "no auto reversal", "concurrency lock", "risk permission", "block reason")
EXECUTION_FIELDS = ("paper_only", "entry intent", "fill type", "slippage", "commission", "funding", "stop status", "position status", "live_order_sent")
CONTROL_BUTTONS = ("START", "PAUSE", "STOP NEW ENTRIES", "PANIC", "MANUAL CLOSE", "MUHASEBE KONTROLÜ", "DIAGNOSTIC PACKAGE", "SAFE MODE / REPAIR")
LAYOUT_SECTIONS = ("SIDEBAR_NAVIGATION", "TOP_STATUS_BAR", "SUMMARY_CARDS", "SCANNER", "MARKET_CANDIDATES", "CHART_AREA", "INTELLIGENCE_DECISION", "CANDIDATE_PIPELINE", "RISK_WALLET_POSITION", "PAPER_EXECUTION", "LEDGER_PNL", "TRADE_HISTORY", "REALTIME_EVENT_FLOW", "SYSTEM_HEALTH", "READINESS_CHECKLIST")
SUMMARY_CARDS = ("CÜZDAN ÖZETİ", "PnL ÖZETİ", "CANLI TARAMA ÖZETİ", "RAPOR ÖZETİ", "AÇIK POZİSYONLAR")
SIDEBAR_ITEMS = ("Dashboard / Ana Sayfa", "Trade", "Report", "Optimization", "Health / Diagnostic", "Settings", "Logs / Event Flow")
PIPELINE_STAGES = ("SCAN", "SIGNAL", "CANDIDATE", "RANKED", "SIZED", "RISK CHECK", "READY / BLOCKED", "PAPER EXECUTION", "LEDGER")
EVENT_FLOW_FIELDS = ("Scheduler started", "Waiting closed candle", "Closed candle detected", "Indicator calculated", "No signal", "Candidate found", "Candidate ranked", "Sizing PASS/FAIL", "Risk ALLOW/BLOCK", "Paper execution", "Ledger written", "Health warning", "Repair/diagnostic event", "Live-lock warning")
HEALTH_FIELDS = ("Binance API", "Market data", "DB/record", "Recovery", "Workers/scheduler", "Telegram", "Live-lock", "Last closed candle scan", "Latest error", "Repair mode", "Diagnostic package", "STOP_AND_REPORT")
CONTROL_CENTER_SCREENS = ("Genel Bakış", "Canlı Tarama", "Sinyaller", "Açık Pozisyonlar", "İşlem Geçmişi", "Grafikler", "Strateji", "Risk", "Sistem Sağlığı", "Raporlar", "Bildirimler")
REPORT_TABS = ("Rapor Merkezi", "Portföy Analiz Raporu", "Performans Analizi", "İşlem Analizi", "Risk Merkezi", "Strateji Raporları", "Özel Raporlar")
READINESS_CHECKS = ("Recovery gate PASS", "KONU-1→50 LOCKED", "Faz-0→20 PASS / LOCKED", "LIVE_TRADING=false", "Gerçek emir endpoint yok", "Paper mode ready", "Config loaded", "Scheduler ready", "Closed candle authority ready", "Ledger ready", "Health acceptable", "Kritik açık issue yok", "Snapshot/checkpoint ready")

@dataclass(frozen=True)
class UIIntent:
    action: str
    paper_only: bool = True
    live_order_sent: bool = False
    requires_confirmation: bool = False

@dataclass(frozen=True)
class ControlCenterModel:
    top_status: dict[str, str]
    market_columns: tuple[str, ...] = MARKET_COLUMNS
    state_lifecycle: tuple[str, ...] = STATE_LIFECYCLE
    intelligence_fields: tuple[str, ...] = INTELLIGENCE_FIELDS
    risk_fields: tuple[str, ...] = RISK_FIELDS
    execution_fields: tuple[str, ...] = EXECUTION_FIELDS
    control_buttons: tuple[str, ...] = CONTROL_BUTTONS
    layout_sections: tuple[str, ...] = LAYOUT_SECTIONS
    summary_cards: tuple[str, ...] = SUMMARY_CARDS
    sidebar_items: tuple[str, ...] = SIDEBAR_ITEMS
    pipeline_stages: tuple[str, ...] = PIPELINE_STAGES
    readiness_checks: tuple[str, ...] = READINESS_CHECKS
    event_flow_fields: tuple[str, ...] = EVENT_FLOW_FIELDS
    health_fields: tuple[str, ...] = HEALTH_FIELDS
    screens: tuple[str, ...] = CONTROL_CENTER_SCREENS
    report_tabs: tuple[str, ...] = REPORT_TABS
    active_screen: str = "Genel Bakış"
    active_report_tab: str = "Rapor Merkezi"
    live_controls_visible: bool = True
    live_controls_passive: bool = True
    live_controls_locked: bool = True
    paper_mode_label: str = "PAPER MODE"
    optimization_on_main_page: bool = False
    report_excel_on_main_page: bool = False
    telegram_commands_enabled: bool = False
    refresh_interval: timedelta = timedelta(minutes=2)

    def display_refresh(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        return {"display_snapshot": snapshot, "decision_allowed": False, "execution_triggered": False}

    def intent(self, action: str) -> UIIntent:
        if action not in self.control_buttons:
            raise ValueError(f"Unknown UI action: {action}")
        return UIIntent(action, requires_confirmation=action in {"PANIC", "MANUAL CLOSE"})

    def readiness(self, checks: dict[str, bool]) -> dict[str, Any]:
        passed = all(checks.get(item, False) for item in self.readiness_checks)
        return {"passed": passed, "paper_start_intent_allowed": passed, "checks": checks}

    def bind_snapshot(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        """Expose module-owned data without creating a second decision authority."""
        return {"snapshot": snapshot, "source": "ledger/status modules", "decision_allowed": False}

def build_control_center(now: datetime | None = None) -> ControlCenterModel:
    now = now or datetime.now()
    return ControlCenterModel({
        "algorithm": "ALGORİTMİK TRADE PRO / TILSON T3", "mode": "PAPER",
        "market": "BINANCE USDT-M FUTURES", "data": "RAW / CLOSED CANDLE",
        "engine": "PAPER ONLY", "scheduler": "ACTIVE", "health": "GREEN",
        "clock": now.isoformat(),
    })
