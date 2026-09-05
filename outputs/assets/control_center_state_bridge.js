(function () {
  "use strict";
  const base = "http://127.0.0.1:8765/api/paper";
  const viewModelEndpoint = base + "/view-model";
  const text = (selector, value) => { const node = document.querySelector(selector); if (node) node.textContent = value; };
  function render(vm) {
    document.documentElement.dataset.uiConnected = "true";
    text("[data-paper-ui-status]", "UI CONNECTED: YES · PAPER LOCAL STATE");
    text("[data-paper-runtime]", vm.runtime.paper_runtime);
    text("[data-paper-wallet-equity]", Number(vm.wallet.equity_usd).toFixed(2));
    text("[data-paper-total-pnl]", Number(vm.wallet.total_pnl_usd).toFixed(2));
    text("[data-paper-position-count]", String((vm.positions.positions || []).length));
    text("[data-paper-order-count]", String((vm.open_orders.open_orders || []).length));
    text("[data-paper-health]", vm.health.paper_state + " / " + vm.health.runtime_worker);
    text("[data-paper-safety]", "REAL_ORDER_BLOCKED · LIVE_LOCKED");
    const cards = document.querySelectorAll(".cards > .panel");
    const walletValues = cards[0] && cards[0].querySelectorAll(".kv b");
    if (walletValues && walletValues.length >= 8) { [vm.wallet.initial_wallet_usd, vm.wallet.equity_usd, vm.wallet.available_usd, vm.wallet.used_margin_usd, 0, vm.wallet.realized_pnl_usd, vm.wallet.unrealized_pnl_usd, vm.wallet.total_pnl_usd].forEach((v, i) => walletValues[i].textContent = Number(v).toFixed(2)); }
    if (cards[1]) { const pnl = cards[1].querySelectorAll(".kv b"); if (pnl.length >= 5) { pnl[0].textContent = Number(vm.wallet.realized_pnl_usd).toFixed(2); pnl[1].textContent = Number(vm.wallet.unrealized_pnl_usd).toFixed(2); pnl[4].textContent = Number(vm.wallet.total_pnl_usd).toFixed(2); } }
    const positionsBody = document.querySelector(".positions-scroll tbody"); if (positionsBody) positionsBody.innerHTML = (vm.positions.positions || []).length ? "" : '<tr><td colspan="8">NO PAPER POSITIONS</td></tr>';
    const historyBody = document.querySelector(".trade-history-scroll tbody"); if (historyBody) historyBody.innerHTML = (vm.ledger.closed_trades || []).length ? "" : '<tr><td colspan="6">NO PAPER TRADES</td></tr>';
    const eventBody = document.querySelector(".event-scroll tbody"); if (eventBody) eventBody.innerHTML = (vm.events.events || []).map((e) => '<tr><td>PAPER</td><td>EVENT</td><td colspan="8">' + String(e.type) + '</td></tr>').join("");
  }
  function disconnected() { document.documentElement.dataset.uiConnected = "false"; text("[data-paper-ui-status]", "UI CONNECTED: NO · LOCAL SERVER REQUIRED"); text("[data-paper-safety]", "STATE NOT CONNECTED · REAL_ORDER_BLOCKED · LIVE_LOCKED"); document.querySelectorAll(".cards .kv b").forEach((n) => n.textContent = "STATE NOT CONNECTED"); const p = document.querySelector(".positions-scroll tbody"); if (p) p.innerHTML = '<tr><td colspan="8">LOCAL SERVER OFF / STATE NOT CONNECTED</td></tr>'; const h = document.querySelector(".trade-history-scroll tbody"); if (h) h.innerHTML = '<tr><td colspan="6">LOCAL SERVER OFF / STATE NOT CONNECTED</td></tr>'; }
  async function refresh() { try { const response = await fetch(viewModelEndpoint); if (!response.ok) throw new Error("state"); render(await response.json()); } catch (_) { disconnected(); } }
  async function action(path) { try { await fetch(base + path, { method: "POST" }); } finally { refresh(); } }
  document.addEventListener("DOMContentLoaded", function () {
    const commands = document.querySelectorAll(".commands button");
    if (commands[0]) { commands[0].disabled = false; commands[0].dataset.paperStop = "true"; }
    if (commands[1]) { commands[1].disabled = false; commands[1].dataset.paperStart = "true"; }
    if (commands[4]) commands[4].dataset.paperRuntime = "true";
    document.querySelectorAll("[data-paper-start]").forEach((b) => b.addEventListener("click", () => action("/start")));
    document.querySelectorAll("[data-paper-stop]").forEach((b) => b.addEventListener("click", () => action("/stop")));
    if (!document.querySelector("[data-paper-ui-status]")) { const banner = document.createElement("div"); banner.dataset.paperUiStatus = "true"; banner.style.cssText = "position:fixed;bottom:4px;left:240px;z-index:5;color:#00d8ff;font:12px monospace"; document.body.appendChild(banner); }
    refresh(); setInterval(refresh, 120000);
  });
})();
