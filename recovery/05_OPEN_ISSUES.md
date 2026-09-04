# Tilson T3 — Open Issues

## GÜN SONU KAPANIŞ — 2026-09-03

- Day-end snapshot: `snapshots/day_end_close_reverted_safe_point_10_17_pending_20260903_0432.txt` (SHA-256 `A06D9AA89F47968B74A8A0043FB913179EAFAC47ADC4F31E15D299A562A8BB77`).
- 10–17 mevcut HTML çıktıları yalnız `UNACCEPTED_WORKING_ARTIFACTS` olarak tutulur; PASS, APPROVED, LOCKED veya BASELINE_PROTECTED değildir.
- 10–17 için `NOT_ACCEPTED / REWORK_PENDING / USER_LATER_QA_REQUIRED` ve ileride kullanıcı browser/manual QA şartı geçerlidir.
- Safe point `REVERTED_TO_GROUP2_APPROVED_STATE` olarak korunur; 01–09 `DO_NOT_TOUCH` kapsamındadır.

Control Center fiili seti 17 ekrandır: 01 = Genel Bakış; 02–17 = diğer Control Center ekranları. “Genel Bakış + 1–17” çalışma bütününü anlatır; ayrı 18. ekran yoktur.

## Güncel açık konular — Faz-21→47

- Grup-2 / 06–09: USER_QA_APPROVED_WITH_FONT_READABILITY_AND_SCALE_NOTE.
- Grup-2 kabul edilirse PASS kaydı yapılacaktır; mevcut kayıtta PASS_RECORDED değildir.
- Grup-3 / 10–13: PENDING.
- Grup-4 / 14–17: PENDING.
- Data binding: NOT_DONE.
- Paper: OFF. Live: OFF / LOCKED.
- Word/DOCX render QA gerekiyorsa ayrı kullanıcı onayı ve desteklenen render ortamı gerekir.

Kaynak: `recovery/word/Tilson_T3_05_Open_Issues_Kilitli.docx`.

**KONU-1 → KONU-50 kilitli; kritik açık issue yok.**

Yeni belirsizlik veya çelişki çıkarsa ilerleme durdurulur, konu açılır ve `STOP_AND_REPORT` uygulanır.

## RECOVERY CONSISTENCY REPAIR — CURRENT SAFE POINT

- Current safe point: **REVERTED_TO_GROUP2_APPROVED_STATE**.
- Basis: **GROUP2_USER_QA_APPROVED_WITH_FONT_READABILITY_AND_SCALE_NOTE_RECORDED**.
- 10–17 outputs are **NOT_ACCEPTED**. Failed attempts were reverted; 10–17 are **REWORK_PENDING**.
- No previous 10–17 attempt is accepted as baseline.
- Faz-21 remains **IN_PROGRESS**: 01 PASS recorded; 02–05 protected; 06–09 approved with final readability note; 10–17 pending rework.

## Faz-14 blocker

- `@oai/artifact-tool` çalışma ortamında mevcut değil.
- `.xlsx` export oluşturma/doğrulaması yapılamıyor.
- Report modeli, filtreler, Ledger kaynak kontrolü ve Excel export uygulanmadı.
- Durum: **Çözüldü — KONU-49 ile Faz-14 için `openpyxl` onaylandı.**
- openpyxl 3.1.5 doğrulandı; eski artifact-tool blocker tarihsel kayıt olarak korunur.
- Kritik açık issue yok.

KONU-50: LOCKED. Faz-21 → Faz-47 planı kayıtlıdır ve kullanıcı onayıyla STARTED / IN_PROGRESS durumundadır.
- Artifact-tool blocker: çözüldü; openpyxl 3.1.5 doğrulandı.
- Word/DOC final paket içerik güncellemesi tamamlandı; varsa görsel render QA ayrı konudur.
- Render QA blocker: pdf2image ve LibreOffice/soffice mevcut değil.
- Çözüm: Render destekli ortam sağlandığında 12 DOCX için görsel QA yeniden çalıştırılacak.
- Render QA durumu: BLOCKED / WAITING_RENDER_ENV.
- Faz-14 export doğrulaması tamamlandı; blocker kapalı, Faz-14 PASS / LOCKED.

## FAZ-21 / 01-17 USER VISUAL QA + TECHNICAL STATIC PASS - 2026-09-04

- User visual QA: 01-17 USER_VISUAL_QA_APPROVED.
- Technical static validation: 17/17 PASS.
- UTF-8: 17/17 PASS.
- U+FFFD replacement character: 0.
- Mojibake pattern: NONE.
- 01 metadata: data-live-order-sending-allowed="false" added.
- 07 Strategy: four help ? icons removed by user request.
- Duplicate shell check: USER_VISUAL_QA_CONFIRMED / AUTOMATED_CHECK_INCONCLUSIVE / ACCEPTED_FOR_FAZ21_STATIC_UI_SCOPE.
- 01-17: USER_VISUAL_QA_APPROVED / TECHNICAL_STATIC_PASS / RECORDED.
- Faz-21: UI_SCREEN_SCOPE_17_17_PASS / WAITING_FAZ21_EXIT_GATE.
- Data binding: NOT_DONE.
- Paper: OFF.
- Live: OFF / LOCKED.
- LIVE_TRADING=false.
- live_order_sending_allowed=false.
- Real order/Binance order endpoint: NONE.
- Faz-22: NEXT_PENDING_USER_APPROVAL.
- Note: This is UI visual/static scope record; it is not paper start.

## FAZ-21 EXIT GATE PASS / CLOSED - 2026-09-04

- Faz-21 result: PASS / LOCKED.
- Exit gate: FAZ21_EXIT_GATE_PASS.
- 01-17 UI screens: USER_VISUAL_QA_APPROVED / TECHNICAL_STATIC_PASS / RECORDED.
- Recovery record: ASCII-only PASS.
- Report exists: reports/faz21_ui_01_17_user_visual_qa_and_technical_pass_report.json.
- Snapshot exists: snapshots/faz21_ui_01_17_user_visual_qa_technical_pass_20260904_1649.txt.
- Note: Previous snapshot may contain Turkish mojibake; it is preserved as historical artifact and not edited.
- New closure records are ASCII-only.
- Data binding: NOT_DONE.
- Paper: OFF.
- Live: OFF / LOCKED.
- LIVE_TRADING=false.
- live_order_sending_allowed=false.
- Real order/Binance order endpoint: NONE.
- Faz-22: NEXT_PENDING_USER_APPROVAL.
- Note: Faz-21 closure is UI visual/static scope closure only. It is not paper start.
+## FAZ-22C READ-ONLY RUNTIME STATUS ADAPTER GATE READY - 2026-09-04

- Faz-22C gate result: FAZ22C_READ_ONLY_ADAPTER_GATE_READY.
- Scope: gate/design readiness only.
- Implementation: NOT_STARTED.
- Proposed adapter file: src/ui/control_center/runtime_status_adapter.py.
- Proposed test file: tests/test_runtime_status_adapter.py.
- Adapter rule: read-only snapshot only.
- Adapter must not start paper, live, server, scheduler loop, bridge, execution, or network/order endpoint.
- Adapter must not call src/paper/execution.py.
- Adapter must read live-lock config and expose LIVE_TRADING=false and live_order_sending_allowed=false.
- Missing runtime sources must return UNKNOWN / OFF / STALE / BLOCKED.
- Data binding status remains DESIGN_READY / NOT_IMPLEMENTED.
- Runtime backend/service: NOT_READY.
- Paper orchestration: NOT_READY.
- Ledger persistence: NOT_READY.
- Required tests: no execution call, no network/order endpoint, no paper/live start, live-lock fields false, snapshot compatible with ControlCenterModel.bind_snapshot().
- Blockers: no completed runtime status adapter, no runtime source registry, no persistent ledger store, no scheduler/status loop.
- Safe next step: FAZ-22C narrow implementation package with read-only adapter and tests only, after explicit user approval.
- Paper: OFF.
- Live: OFF / LOCKED.
- LIVE_TRADING=false.
- live_order_sending_allowed=false.
- Real order/Binance order endpoint: NONE.
- Note: This record is gate/readiness only. It is not implementation, paper start, server start, or live enable.
+## FAZ-22C READ-ONLY RUNTIME STATUS ADAPTER IMPLEMENTED - 2026-09-04

- Faz-22C result: READ_ONLY_RUNTIME_STATUS_ADAPTER_IMPLEMENTED.
- Scope: narrow implementation only.
- Adapter file: src/ui/control_center/runtime_status_adapter.py.
- Test file: tests/test_runtime_status_adapter.py.
- Adapter rule: read-only snapshot only.
- Paper start: NOT_TRIGGERED.
- Live start: NOT_TRIGGERED.
- Server start: NOT_TRIGGERED.
- Scheduler loop start: NOT_TRIGGERED.
- Execution call: NONE.
- Network/order endpoint: NONE.
- LIVE_TRADING=false.
- live_order_sending_allowed=false.
- Data binding: PARTIAL_READ_ONLY_STATUS_ADAPTER / NOT_FULL_RUNTIME_BINDING.
- Runtime backend/service: NOT_STARTED.
- Paper orchestration: NOT_STARTED.
- Ledger persistence: NOT_STARTED.
- Failure states supported: UNKNOWN / OFF / STALE / BLOCKED.
- Tests: PASS.
- Next subphase: FAZ-22D UI FUNCTIONAL SIMULATION WITHOUT PAPER START.
- Note: This is not paper start, server start, live enable, or real order capability.

## FAZ-22B DATA BINDING DESIGN READY - 2026-09-04

- Faz-22B result: FAZ22B_DATA_BINDING_DESIGN_READY.
- Scope: design/contract only.
- Implementation: NOT_STARTED.
- Data binding status: DESIGN_READY / NOT_IMPLEMENTED.
- Runtime backend/service: NOT_READY.
- Paper orchestration: NOT_READY.
- Ledger persistence: NOT_READY.
- Static UI status: 17/17 screens present.
- Canonical source map prepared for market, candle, strategy, risk, execution, ledger, positions, health, scheduler, reports, and notifications.
- Field contract prepared with: UI field, current source, required canonical source, refresh policy, stale behavior, safety gate, failure state, implementation phase.
- Refresh/stale policy: defined.
- Safety gate map: defined.
- Failure states: BLOCKED / UNKNOWN / STALE / READY / OFF defined.
- Next required subphase: FAZ-22C READ-ONLY RUNTIME STATUS ADAPTER DESIGN/IMPLEMENTATION GATE.
- Paper: OFF.
- Live: OFF / LOCKED.
- LIVE_TRADING=false.
- live_order_sending_allowed=false.
- Real order/Binance order endpoint: NONE.
- Note: This record is design-only. It is not data binding implementation, paper start, server start, or live enable.

## FAZ-22A FUNCTIONAL GAP ANALYSIS READY - 2026-09-04

- Faz-21 status: PASS / LOCKED.
- Faz-22 open gate result: STOP / GAP_ANALYSIS_REQUIRED.
- Faz-22A result: FAZ22A_FUNCTIONAL_GAP_ANALYSIS_READY.
- Static UI status: 17/17 screens present.
- Route/local link status: PASS.
- Button status: display-only / disabled PASS.
- Runtime data binding: NOT_DONE.
- Runtime backend/service: NOT_READY.
- Paper orchestration: NOT_READY.
- Ledger persistence: NOT_READY.
- UI state source: sample/static dataset still used in multiple areas.
- Required next subphase: FAZ-22B DATA BINDING DESIGN.
- Required design fields: UI field, canonical source, refresh policy, stale-data behavior, safety gate, failure state.
- Paper: OFF.
- Live: OFF / LOCKED.
- LIVE_TRADING=false.
- live_order_sending_allowed=false.
- Real order/Binance order endpoint: NONE.
- Note: This is analysis/record only. It is not implementation, paper start, server start, or live enable.
