"""Local-only, fail-closed paper state adapter. No market or order network calls."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state" / "paper"
FILES = {"runtime": "runtime_state.json", "wallet": "wallet_state.json", "positions": "positions.json", "open-orders": "open_orders.json", "ledger": "ledger.json", "events": "events.json", "health": "health.json"}

def read_state(name: str):
    return json.loads((STATE / FILES[name]).read_text(encoding="utf-8"))

def view_model():
    runtime, wallet, positions, orders, ledger, events, health = (read_state(k) for k in ("runtime", "wallet", "positions", "open-orders", "ledger", "events", "health"))
    return {"runtime": runtime, "wallet": wallet, "positions": positions, "open_orders": orders, "ledger": {"fills": ledger.get("fills", []), "closed_trades": ledger.get("closed_trades", []), "summary": {"fill_count": len(ledger.get("fills", [])), "closed_trade_count": len(ledger.get("closed_trades", []))}}, "events": events, "health": health, "safety_flags": {"paper_start_allowed": False, "live_locked": True, "real_order_allowed": False}, "ui_status": {"connected": True, "source": "PAPER_LOCAL_STATE"}}

def write_events(event_type: str):
    path = STATE / "events.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("events", []).append({"type": event_type, "status": "RECORDED"})
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

class Handler(BaseHTTPRequestHandler):
    def _send(self, payload, status=200):
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(raw))); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers(); self.wfile.write(raw)
    def do_OPTIONS(self): self._send({}, 204)
    def do_GET(self):
        route = urlparse(self.path).path
        if route == "/api/paper/view-model": return self._send(view_model())
        prefix = "/api/paper/"
        if route.startswith(prefix) and route[len(prefix):] in FILES: return self._send(read_state(route[len(prefix):]))
        self._send({"error": "NOT_FOUND"}, 404)
    def do_POST(self):
        route = urlparse(self.path).path
        if route == "/api/paper/start":
            write_events("START_REQUEST_BLOCKED")
            return self._send({"result": "START_BLOCKED_PERMISSION_REQUIRED", "paper_start_allowed": False}, 403)
        if route == "/api/paper/stop":
            runtime_path = STATE / "runtime_state.json"; runtime = json.loads(runtime_path.read_text(encoding="utf-8")); runtime["paper_runtime"] = "OFF"; runtime["last_action"] = "PAPER_STOP_REQUEST_RECORDED"; runtime_path.write_text(json.dumps(runtime, indent=2) + "\n", encoding="utf-8"); write_events("PAPER_STOP_REQUEST_RECORDED"); return self._send({"result": "PAPER_STOP_REQUEST_RECORDED", "paper_runtime": "OFF"})
        self._send({"error": "NOT_FOUND"}, 404)
    def log_message(self, *_): pass

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
