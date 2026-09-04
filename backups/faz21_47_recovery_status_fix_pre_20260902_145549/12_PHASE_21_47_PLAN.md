# Tilson T3 — Faz-21 → Faz-47 Detaylı İş Akışı

Durum: LOCKED plan kaydı; Faz-21 ve sonrası NOT_STARTED, kullanıcı onayı gerekir.

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

Live trading kapalıdır: LIVE_TRADING=false. Gerçek Binance order endpoint’i eklenemez. Faz-21 → Faz-47 uygulaması başlatılmamıştır.
