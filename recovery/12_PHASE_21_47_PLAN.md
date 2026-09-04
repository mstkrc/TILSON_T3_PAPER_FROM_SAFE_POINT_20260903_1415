# Tilson T3 — Faz-21 → Faz-47 Detaylı İş Akışı

Durum: LOCKED plan kaydı korunuyor; Faz-21→47 uygulama süreci kullanıcı onayıyla STARTED / IN_PROGRESS durumundadır. `01_GENEL_BAKIS` PASS kaydedildi. UI modüler yapı hazırlandı. Grup-1 / 02–05 baseline protected durumundadır. Grup-2 / 06–09: USER_QA_APPROVED_WITH_FONT_READABILITY_AND_SCALE_NOTE. Grup-3 / 10–13 ve Grup-4 / 14–17: NOT_ACCEPTED / REVERTED / REWORK_PENDING. Data binding yapılmadı. Paper/live kapalıdır.

KONU-50, UI’yi tam operasyon merkezi olarak doğrulamayı; UI functional PASS, paper stability PASS ve ayrı Live Gate olmadan ilerlememeyi zorunlu kılar. Ledger tek kaynak, Recovery Gate ve STOP_AND_REPORT her aşamada geçerlidir.

| Faz | Kapsam | Çıkış ilkesi |
|---|---|---|
| 21–26 | UI cockpit, functional, decision explanation, safety/live-lock, Ledger/PnL/position, error/repair/diagnostic review | Eksik veya açıklanamayan durum FAIL/BLOCKED/STOP_AND_REPORT |
| 27 | Paper Start Readiness Audit | 10/10 PASS olmadan paper start yok |
| 28–32 | Paper start, first closed candle, candidate/no-trade, first paper entry/exit | Closed candle, açıklanabilir event flow ve Ledger uyumu zorunlu |
| 33–35 | End-of-day, multi-day stability, failure/recovery drill | Kritik hata, ledger blocking error, open-candle decision ve gerçek emir denemesi sıfır |
| 36–38 | Behavior/risk review, config tuning gate, post-tuning regression | Otomatik tuning/direct apply yok; kullanıcı onayı zorunlu |
| 39–42 | Paper promotion, Live Readiness Audit, Live Gate Design, dry-run/no-order | Ayrı Live Gate ve 10/10 PASS olmadan gerçek emir yok |
| 43–47 | Micro approval, first micro live, audit, stabilization, scale/pause/repair decision | Açık kullanıcı onayı ve her büyütmede yeni onay zorunlu |

Güncel uygulama alt durumu:

- `01_GENEL_BAKIS`: PASS / RECORDED.
- `UI_MODULAR_SPLIT`: READY.
- Grup-1 / 02–05: IMPLEMENTED / USER_QA_REVIEWED.
- Grup-2 / 06–09: USER_QA_APPROVED_WITH_FONT_READABILITY_AND_SCALE_NOTE.
- Grup-3 / 10–13 ve Grup-4 / 14–17: NOT_ACCEPTED / REVERTED / REWORK_PENDING.
- 01–09: BASELINE_PROTECTED / DO_NOT_TOUCH.
- 10–17: NOT BASELINE / NOT ACCEPTED / REWORK ONLY AFTER USER APPROVAL.
- Data binding: NOT_DONE.
- Paper: OFF.
- Live: OFF / LOCKED.

Current safe point: REVERTED_TO_GROUP2_APPROVED_STATE.
Day-end close: `DAY_END_CLOSE_COMPLETED_REVERTED_SAFE_POINT_10_17_PENDING`.
Day-end reference: `snapshots/day_end_close_reverted_safe_point_10_17_pending_20260903_0432.txt`.
Day-end reference SHA-256: `A06D9AA89F47968B74A8A0043FB913179EAFAC47ADC4F31E15D299A562A8BB77`.
Control Center fiili seti 17 ekrandır: 01 = Genel Bakış; 02–17 = diğer Control Center ekranları. “Genel Bakış + 1–17” çalışma bütününü anlatır; ayrı 18. ekran yoktur.

Live trading kapalıdır: `LIVE_TRADING=false`, `live_order_sending_allowed=false`. Gerçek Binance/order endpoint yoktur.

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
