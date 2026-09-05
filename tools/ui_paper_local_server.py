"""Local-only paper UI API; no market/private API or real order capability."""
from __future__ import annotations
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state" / "paper"
FILES = {"runtime":"runtime_state.json","wallet":"wallet_state.json","positions":"positions.json","open-orders":"open_orders.json","ledger":"ledger.json","events":"events.json","health":"health.json","notifications":"notifications.json","strategy":"strategy.json","risk":"risk.json","scanner":"scanner.json","reports":"reports.json","ui-selection":"ui_selection.json","pending-change-requests":"pending_change_requests.json","pending-panic-confirmations":"pending_panic_confirmations.json","trade-loop":"trade_loop_state.json"}

def read(name): return json.loads((STATE / FILES[name]).read_text(encoding="utf-8"))
def write(name, value): (STATE / FILES[name]).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
read_state = read
def event(kind, **extra):
    data = read("events"); data.setdefault("events", []).append({"type": kind, **extra}); write("events", data)
def body(handler):
    size = int(handler.headers.get("Content-Length", "0")); return json.loads(handler.rfile.read(size) or b"{}")
def vm():
    names = ("runtime","wallet","positions","open-orders","ledger","events","health","notifications","strategy","risk","scanner","reports","ui-selection","trade-loop")
    data = {n.replace("-", "_"): read(n) for n in names}; ledger = data["ledger"]
    data["ledger"]["summary"] = {"fill_count": len(ledger.get("fills", [])), "closed_trade_count": len(ledger.get("closed_trades", []))}
    data["safety"] = {"paper_start_allowed": data["runtime"].get("paper_start_allowed", False), "live_locked": True, "LIVE_TRADING": False, "live_order_sending_allowed": False, "real_order_allowed": False}
    scan = json.loads((STATE / "scan_results.json").read_text(encoding="utf-8")) if (STATE / "scan_results.json").exists() else {}
    cursor = json.loads((STATE / "universe_scan_cursor.json").read_text(encoding="utf-8")) if (STATE / "universe_scan_cursor.json").exists() else {}
    data["scan_summary"] = {"universe_enabled": True, "universe_size": cursor.get("universe_size", scan.get("total_symbols", 0)), "batch_size": cursor.get("batch_size", 0), "next_index": cursor.get("next_index", 0), "symbols_scanned_this_round": cursor.get("symbols_scanned_this_round", scan.get("scanned_symbols", 0)), "data_pass": scan.get("data_pass", 0), "data_fail": scan.get("data_fail", 0), "no_signal": scan.get("no_signal", 0), "long_signal": scan.get("long_signal", 0), "short_signal": scan.get("short_signal", 0), "candidates": scan.get("candidate_count", 0), "risk_allow": scan.get("risk_allow_count", 0), "risk_block": scan.get("risk_block_count", 0), "paper_orders": scan.get("paper_order_count", 0), "status": cursor.get("status", "IDLE")}
    data["safety_flags"] = {"real_order_allowed": False, "live_trading": False, "live_order_sending_allowed": False}
    data["ui_status"] = {"connected": True, "source": "PAPER_LOCAL_STATE", "trade_decision_generated": False}; return data
view_model = vm

class Handler(BaseHTTPRequestHandler):
    def send_json(self, value, status=200):
        raw = json.dumps(value).encode(); self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(raw))); self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers(); self.wfile.write(raw)
    def do_OPTIONS(self): self.send_json({}, 204)
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/paper/trade-loop/status": return self.send_json(read("trade-loop"))
        if path in ("/api/ui/view-model", "/api/paper/view-model"): return self.send_json(vm())
        if path == "/api/ui/screens": return self.send_json({"screens": [f"{i:02d}" for i in range(1, 18)]})
        if path == "/api/ui/detail": return self.send_json({"selected": read("ui-selection")})
        relative = unquote(path.lstrip("/")) or "faz21_control_center.html"
        candidate = (ROOT / relative).resolve()
        if not candidate.is_file():
            candidate = (ROOT / "outputs" / relative).resolve()
        if candidate.is_file() and ROOT in candidate.parents and candidate.suffix.lower() in {".html", ".js", ".css", ".svg", ".json"}:
            raw = candidate.read_bytes(); self.send_response(200); self.send_header("Content-Type", mimetypes.guess_type(str(candidate))[0] or "application/octet-stream"); self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw); return
        prefix = "/api/paper/"; key = path[len(prefix):] if path.startswith(prefix) else ""
        if key in FILES: return self.send_json(read(key))
        self.send_json({"error":"NOT_FOUND"}, 404)
    def do_POST(self):
        path = urlparse(self.path).path; payload = body(self)
        if path == "/api/paper/trade-loop/status": return self.send_json(read("trade-loop"))
        if path == "/api/paper/trade-loop/run-once":
            from paper_trade_loop_runner import cycle
            return self.send_json({"ok": True, "result": cycle()})
        if path == "/api/paper/trade-loop/start":
            s=read("trade-loop"); s["paper_trade_loop_allowed"]=True; s["paper_trade_loop_status"]="START_REQUESTED"; write("trade-loop",s); event("PAPER_TRADE_LOOP_START_REQUESTED"); return self.send_json({"ok": True, "result":"PAPER_TRADE_LOOP_BACKGROUND_RUNNER_NOT_IMPLEMENTED","run_once":"/api/paper/trade-loop/run-once"})
        if path == "/api/paper/trade-loop/stop":
            s=read("trade-loop"); s["paper_trade_loop_allowed"]=False; s["paper_trade_loop_status"]="OFF"; write("trade-loop",s); event("PAPER_TRADE_LOOP_STOPPED"); return self.send_json({"ok": True, "result":"PAPER_TRADE_LOOP_STOPPED"})
        if path == "/api/paper/start":
            r=read("runtime")
            if not r.get("paper_start_allowed",False): event("START_REQUEST_BLOCKED", reason="USER_PAPER_PERMISSION_REQUIRED"); return self.send_json({"result":"START_BLOCKED_PERMISSION_REQUIRED","paper_start_allowed":False}, 403)
            r.update({"paper_runtime":"ON","mode":"PAPER","live_runtime":"OFF_LOCKED","real_order_allowed":False,"live_order_sending_allowed":False,"last_action":"PAPER_LOCAL_RUNTIME_STARTED"}); write("runtime",r); event("PAPER_LOCAL_RUNTIME_STARTED"); return self.send_json({"result":"PAPER_LOCAL_RUNTIME_STARTED","paper_runtime":"ON","mode":"PAPER","live_runtime":"OFF_LOCKED"})
        if path == "/api/paper/stop":
            r = read("runtime"); r.update({"paper_runtime":"OFF","last_action":"PAPER_STOP_REQUEST_RECORDED"}); write("runtime", r); event("PAPER_STOP_REQUEST_RECORDED"); return self.send_json({"result":"PAPER_STOP_REQUEST_RECORDED","paper_runtime":"OFF"})
        if path == "/api/paper/manual-close": return self.close_position(payload)
        if path == "/api/paper/cancel-order": return self.cancel_order(payload)
        if path == "/api/paper/panic-request":
            p=read("pending-panic-confirmations"); p["requests"].append({"id":"PANIC_PENDING","status":"AWAITING_CONFIRMATION"}); write("pending-panic-confirmations",p); event("PANIC_REQUEST_RECORDED"); return self.send_json({"result":"PANIC_CONFIRMATION_REQUIRED"})
        if path == "/api/paper/panic-confirm": return self.panic_confirm()
        if path == "/api/ui/action": return self.ui_action(payload)
        if path == "/api/ui/refresh": event("UI_REFRESH_REQUESTED"); return self.send_json(vm())
        if path == "/api/strategy/config-change-request": return self.config_request(payload)
        if path == "/api/reports/open": return self.report_action(payload, "open_report")
        if path == "/api/reports/export": return self.send_json({"ok": False, "error": "EXPORT_NOT_IMPLEMENTED"}, 501)
        if path == "/api/ui/selection": return self.ui_action({**payload, "action": "select_row"})
        if path == "/api/ui/detail": return self.ui_action({**payload, "action": "open_detail"})
        if path == "/api/ui/change-request": return self.config_request(payload)
        if path == "/api/notification/mark-read": event("NOTIFICATION_MARK_READ_REQUESTED", notification_id=payload.get("notification_id")); return self.send_json({"result":"NOTIFICATION_MARK_READ_RECORDED"})
        self.send_json({"error":"NOT_FOUND"}, 404)
    def config_request(self, payload):
        p=read("pending-change-requests"); p["requests"].append({"action":"strategy_config_change_request","payload":payload,"requires_user_confirmation":True}); write("pending-change-requests",p); event("STRATEGY_CONFIG_CHANGE_REQUESTED"); return self.send_json({"result":"CONFIG_CHANGE_PENDING_USER_CONFIRMATION"})
    def close_position(self, payload):
        positions=read("positions").get("positions",[]); found=next((p for p in positions if p.get("id")==payload.get("position_id") or p.get("symbol")==payload.get("symbol")),None)
        if not found: event("MANUAL_CLOSE_BLOCKED", reason="POSITION_NOT_OPEN"); return self.send_json({"result":"MANUAL_CLOSE_BLOCKED_POSITION_NOT_OPEN"},409)
        event("MANUAL_CLOSE_REQUEST_RECORDED", position_id=payload.get("position_id")); return self.send_json({"result":"MANUAL_CLOSE_RECORDED_NO_EXECUTION"})
    def cancel_order(self, payload):
        orders=read("open-orders").get("open_orders",[]); order=next((o for o in orders if o.get("id")==payload.get("order_id")),None)
        if not order: event("CANCEL_ORDER_BLOCKED", reason="ORDER_NOT_FOUND"); return self.send_json({"result":"CANCEL_BLOCKED_ORDER_NOT_FOUND"},409)
        if str(order.get("status","")).upper() == "FILLED": event("CANCEL_ORDER_BLOCKED", reason="ORDER_FILLED"); return self.send_json({"result":"CANCEL_BLOCKED_ORDER_FILLED"},409)
        order["status"]="CANCELED"; write("open-orders",{"open_orders":orders}); event("CANCEL_ORDER_RECORDED", order_id=order.get("id")); return self.send_json({"result":"CANCEL_RECORDED"})
    def panic_confirm(self):
        positions=read("positions").get("positions",[]); open_positions=[p for p in positions if p.get("is_open",True)]
        if not open_positions: event("PANIC_CONFIRMED_NO_OPEN_POSITIONS"); return self.send_json({"result":"PANIC_CONFIRMED_NO_OPEN_POSITIONS"})
        for p in open_positions: p["is_open"]=False
        write("positions",{"positions":positions}); event("PANIC_CLOSE_RECORDED", count=len(open_positions)); return self.send_json({"result":"PANIC_CLOSE_RECORDED_NO_EXECUTION","count":len(open_positions)})
    def ui_action(self, payload):
        action=payload.get("action")
        if action in {"open_detail","select_row","select_chart_symbol"}:
            s=read("ui-selection"); s.update({k:payload.get(k,s.get(k)) for k in ("screen_id","entity_type","entity_id","symbol")}); write("ui-selection",s); event("UI_SELECTION_UPDATED",action=action); return self.send_json({"result":"UI_SELECTION_UPDATED","selection":s})
        if action == "request_edit": return self.config_request(payload)
        if action in {"refresh_view_model","refresh"}: return self.send_json(vm())
        if action in {"open_report","export_report"}: event("REPORT_ACTION_RECORDED",action=action,report_id=payload.get("report_id")); return self.send_json({"result":"REPORT_ACTION_RECORDED"})
        if action in {"manual_close","manual_close_position"}: return self.close_position(payload)
        if action == "cancel_order": return self.cancel_order(payload)
        if action == "mark_notification_read": event("NOTIFICATION_MARK_READ_REQUESTED",notification_id=payload.get("notification_id")); return self.send_json({"result":"NOTIFICATION_MARK_READ_RECORDED"})
        return self.send_json({"result":"UI_ACTION_REJECTED_UNKNOWN_CONTRACT_ACTION"},400)
    def report_action(self, payload, action):
        report_id = payload.get("report_id")
        if report_id and not (ROOT / "reports" / str(report_id)).exists():
            return self.send_json({"ok": False, "error": "REPORT_NOT_FOUND"}, 404)
        event("REPORT_ACTION_RECORDED", action=action, report_id=report_id)
        return self.send_json({"ok": True, "result": "REPORT_ACTION_RECORDED", "report_id": report_id})
    def log_message(self,*args): pass

if __name__ == "__main__": HTTPServer(("127.0.0.1",8765),Handler).serve_forever()
