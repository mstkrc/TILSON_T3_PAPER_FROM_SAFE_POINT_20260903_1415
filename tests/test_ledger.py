"""Phase-11 ledger validation; no UI, export, or external order behavior."""

from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
import pytest

from src.paper.ledger import EntryLedgerRecord, ExitLedgerRecord, LedgerIntegrityStatus, PaperLedger, gross_pnl, net_pnl

ROOT = Path(__file__).parents[1]
NOW = datetime(2026, 1, 1, 11, tzinfo=timezone.utc)


def entry(execution_id="e1", ledger_id="l1"):
    return EntryLedgerRecord(ledger_id, execution_id, "BTCUSDT", "LONG", "ENTRY", Decimal("100"), Decimal("2"), 1, "ISOLATED", Decimal("200"), Decimal("200"), Decimal("0.08"), Decimal("1"), Decimal("0"), Decimal("0"), Decimal("-1.08"), {"id": "snap"}, NOW, NOW, NOW, NOW)


def exit_record(execution_id="x1", linked="l1", direction="LONG"):
    return ExitLedgerRecord("lx", linked, execution_id, "BTCUSDT", direction, "EXIT", "T3_EXIT", Decimal("100"), Decimal("110"), Decimal("2"), 1, gross_pnl(direction, Decimal("100"), Decimal("110"), Decimal("2")), Decimal("0.088"), Decimal("0"), Decimal("0"), Decimal("19.912"), {"id": "snap"}, NOW, NOW, NOW, NOW)


def test_entry_exit_and_pnl():
    ledger = PaperLedger()
    assert ledger.append(entry()) == LedgerIntegrityStatus.PASS
    assert ledger.append(exit_record()) == LedgerIntegrityStatus.PASS
    assert gross_pnl("LONG", Decimal("100"), Decimal("110"), Decimal("2")) == Decimal("20")
    assert gross_pnl("SHORT", Decimal("110"), Decimal("100"), Decimal("2")) == Decimal("20")
    assert net_pnl(Decimal("20"), Decimal("0.1"), Decimal("0.2"), Decimal("0.3")) == Decimal("19.4")


def test_duplicates_missing_entry_and_invalid_fields():
    ledger = PaperLedger(); ledger.append(entry())
    with pytest.raises(ValueError, match="DUPLICATE"):
        ledger.append(entry(execution_id="e1", ledger_id="l2"))
    with pytest.raises(ValueError, match="EXIT_WITHOUT_ENTRY"):
        PaperLedger().append(exit_record())
    with pytest.raises(ValueError, match="INVALID_ENTRY"):
        ledger.append(EntryLedgerRecord("bad", "bad", "X", "LONG", "ENTRY", Decimal("0"), Decimal("1"), 1, "ISOLATED", Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), {}, NOW, NOW, NOW, NOW))


def test_snapshot_required_and_live_locked():
    assert entry().config_snapshot
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False
    assert not list((ROOT / "src/paper").glob("*export*"))
