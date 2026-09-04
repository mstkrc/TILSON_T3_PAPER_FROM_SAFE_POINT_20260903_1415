from pathlib import Path

import pytest

from src.ui.control_center.ledger_pnl_position_builder import (
    build_safe_ledger_pnl_position_payload,
    get_ledger_blocked_by,
    get_ledger_fail_closed_reason,
    validate_ledger_pnl_position_payload,
)
from src.ui.control_center.ledger_pnl_position_schema import LEDGER_PNL_POSITION_FIELDS


def _all_ready(**extra):
    base = {"source_freshness": "FRESH", "ledger_consistency": "PASS", "pnl_consistency": "PASS", "position_consistency": "PASS", "overall_consistency": "PASS"}
    base.update(extra)
    return base


def test_default_payload_has_45_fields_and_validates():
    payload = build_safe_ledger_pnl_position_payload()
    assert len(payload.to_dict()) == 45
    assert tuple(payload.to_dict()) == LEDGER_PNL_POSITION_FIELDS
    assert validate_ledger_pnl_position_payload(payload)


def test_safety_defaults_are_false_or_locked():
    values = build_safe_ledger_pnl_position_payload().to_dict()
    assert values["display_only"] is True and values["read_only"] is True
    for name in ("can_write_ledger", "can_mutate_position", "can_recalculate_authoritatively", "can_execute", "can_start_paper", "can_start_live", "can_send_order", "paper_ledger_write_allowed", "live_ledger_write_allowed"):
        assert values[name] is False
    assert values["system_mode"] == "PAPER"
    assert values["ledger_provider_status"] == values["pnl_provider_status"] == values["position_provider_status"] == "PENDING"


@pytest.mark.parametrize("snapshot,expected", [
    (None, "PROVIDER_PENDING"),
    ({"source_freshness": "STALE"}, "PROVIDER_PENDING"),
])
def test_missing_provider_is_highest_priority(snapshot, expected):
    assert get_ledger_fail_closed_reason(build_safe_ledger_pnl_position_payload(snapshot, {}, {}, {})) == expected


def test_fail_closed_priority_and_reasons():
    ready = _all_ready()
    cases = [
        ({"source_freshness": "STALE"}, "STALE_DATA"),
        ({"duplicate_trade_ids_detected": True}, "DUPLICATE_LEDGER_ID"),
        ({"missing_trade_ids_detected": True}, "MISSING_LEDGER_ID"),
        ({"orphan_fills_detected": True}, "ORPHAN_FILL"),
        ({"orphan_positions_detected": True}, "ORPHAN_POSITION"),
        ({"position_ledger_mismatch_detected": True}, "POSITION_LEDGER_MISMATCH"),
        ({"pnl_ledger_mismatch_detected": True}, "PNL_LEDGER_MISMATCH"),
        ({"ledger_consistency": "UNKNOWN"}, "CONSISTENCY_NOT_PROVEN"),
    ]
    for extra, expected in cases:
        merged = dict(ready); merged.update(extra)
        payload = build_safe_ledger_pnl_position_payload(merged, merged, merged, merged)
        assert get_ledger_fail_closed_reason(payload) == expected


def test_clean_ready_payload_has_no_block_reason():
    payload = build_safe_ledger_pnl_position_payload(_all_ready(), _all_ready(), _all_ready(), _all_ready())
    assert get_ledger_fail_closed_reason(payload) == "NONE"
    assert get_ledger_blocked_by(payload) == []
    assert validate_ledger_pnl_position_payload(payload)


def test_injected_authority_and_numeric_values_are_safe_display_values():
    payload = build_safe_ledger_pnl_position_payload(_all_ready(can_execute=True, can_send_order=True, can_start_live=True, can_start_paper=True, can_write_ledger=True, can_mutate_position=True, can_recalculate_authoritatively=True, paper_ledger_write_allowed=True, live_ledger_write_allowed=True, realized_pnl_total=12.5, unrealized_pnl_total=-2.0), {}, {}, {})
    values = payload.to_dict()
    assert all(values[name] is False for name in ("can_execute", "can_send_order", "can_start_live", "can_start_paper", "can_write_ledger", "can_mutate_position", "can_recalculate_authoritatively", "paper_ledger_write_allowed", "live_ledger_write_allowed"))
    assert values["realized_pnl_total"] == 12.5 and values["unrealized_pnl_total"] == -2.0


def test_helpers_return_safe_block_list_and_next_action():
    payload = build_safe_ledger_pnl_position_payload()
    assert get_ledger_fail_closed_reason(payload) == "PROVIDER_PENDING"
    assert get_ledger_blocked_by(payload) == ["PROVIDER_PENDING"]
    assert payload.to_dict()["next_allowed_action"] == "WAIT_FOR_RUNTIME_PROVIDER"


def test_builder_source_has_no_external_clients_or_runtime_writes():
    source = (Path(__file__).parents[1] / "src/ui/control_center/ledger_pnl_position_builder.py").read_text(encoding="utf-8").lower()
    forbidden = ("binance", "requests", "httpx", "websocket", "ccxt", "subprocess", "os.system", "start_server", "uvicorn", "flask", "fastapi", "open(", "write_text", "write_bytes")
    assert not any(item in source for item in forbidden)
