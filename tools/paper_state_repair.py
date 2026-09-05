"""Explicit, paper-only archival reset for invalid sizing artifacts."""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state" / "paper"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--archive-invalid-sizing-artifacts", action="store_true")
    p.add_argument("--confirm-paper-reset", action="store_true")
    a = p.parse_args()
    if not (a.archive_invalid_sizing_artifacts and a.confirm_paper_reset):
        raise SystemExit("EXPLICIT_PAPER_RESET_CONFIRMATION_REQUIRED")
    runtime = json.loads((STATE / "runtime_state.json").read_text())
    if runtime.get("mode") != "PAPER" or runtime.get("live_runtime") != "OFF_LOCKED" or runtime.get("live_trading") or runtime.get("live_order_sending_allowed") or runtime.get("real_order_allowed"):
        raise SystemExit("LIVE_OR_REAL_ORDER_RISK")
    stamp = datetime.now(timezone.utc).isoformat()
    archive = {"archived_at": stamp, "reason": "INVALID_PAPER_SIZING_ARTIFACT", "quantity_source": 'hardcoded Decimal("0.001")', "positions": json.loads((STATE/"positions.json").read_text()), "ledger": json.loads((STATE/"ledger.json").read_text()), "events": json.loads((STATE/"events.json").read_text()), "scan_results": json.loads((STATE/"scan_results.json").read_text()), "safety": runtime, "statement": "These are not valid operational paper positions."}
    out = ROOT / "reports" / "invalid_paper_sizing_artifacts_20260905.json"
    out.write_text(json.dumps(archive, indent=2) + "\n", encoding="utf-8")
    for name, value in (("positions.json", {"positions": [], "source": "PAPER_LOCAL_STATE_RESET"}), ("ledger.json", {"fills": [], "closed_trades": [], "source": "PAPER_LOCAL_LEDGER_RESET"}), ("open_orders.json", {"open_orders": [], "source": "PAPER_LOCAL_STATE_RESET"})):
        (STATE/name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    events = json.loads((STATE/"events.json").read_text())
    events.setdefault("events", []).append({"type":"PAPER_STATE_RESET_AFTER_INVALID_SIZING_ARTIFACT", "timestamp":stamp, "archive":str(out.relative_to(ROOT))})
    (STATE/"events.json").write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")
    print("PAPER_STATE_RESET_AFTER_INVALID_SIZING_ARTIFACT")

if __name__ == "__main__": main()
