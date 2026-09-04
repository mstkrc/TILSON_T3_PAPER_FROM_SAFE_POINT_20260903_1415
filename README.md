# TILSON T3 TRADE

## Proje giriş standardı

Bu proje için authoritative source recovery dokümantasyonudur. Başlangıçta önce resmi recovery okuma sırası izlenir; belirsizlikte çalışma durdurulur ve `STOP_AND_REPORT` uygulanır.

## Resmi recovery okuma sırası

1. `recovery/00_PROJECT_CONSTITUTION.md`
2. `recovery/01_LOCKED_DECISIONS.md`
3. `recovery/02_PHASE_WORKFLOW.md`
4. `recovery/03_LAYER_ARCHITECTURE.md`
5. `recovery/04_CURRENT_STATE.md`
6. `recovery/05_OPEN_ISSUES.md`
7. `recovery/06_RECOVERY_RULES.md`
8. `recovery/10_DOCUMENT_INDEX.md`
9. `recovery/11_PHASE_TRACKER.md`
10. `recovery/12_PHASE_21_47_PLAN.md`

## Current safe point

- Safe point: `REVERTED_TO_GROUP2_APPROVED_STATE`
- Day-end close: `DAY_END_CLOSE_COMPLETED_REVERTED_SAFE_POINT_10_17_PENDING`
- Day-end reference: `snapshots/day_end_close_reverted_safe_point_10_17_pending_20260903_0432.txt`
- Reference SHA-256: `A06D9AA89F47968B74A8A0043FB913179EAFAC47ADC4F31E15D299A562A8BB77`
- Faz-20: `PASS / LOCKED / FOUNDATION_CONFIRMED`
- Faz-21: `IN_PROGRESS / PARTIAL`
- 01–09: `BASELINE_PROTECTED / DO_NOT_TOUCH`
- 06–09: `USER_QA_APPROVED_WITH_FONT_READABILITY_AND_SCALE_NOTE`
- 10–17: `UNACCEPTED_WORKING_ARTIFACTS / NOT_ACCEPTED / REWORK_PENDING / USER_LATER_QA_REQUIRED`

Control Center fiili seti 17 ekrandır: 01 = Genel Bakış; 02–17 = diğer Control Center ekranları. “Genel Bakış + 1–17” çalışma bütününü anlatır; ayrı 18. ekran yoktur.

## Çalışma yöntemi

Kullanıcı onayı olmadan uygulama yapılmaz. Büyük paket yerine küçük kapsam → kontrol → kullanıcı onayı yöntemi kullanılır. Her faz ve kapsam için START GATE, gerekli kontroller, snapshot ve EXIT GATE şartları ayrıca doğrulanır.

01–09 korunur ve değiştirilmez. 10–17 kabul edilmiş baseline sayılmaz; yeni çalışma yalnız yöntem sadeleştirildikten ve kullanıcı onayı alındıktan sonra başlatılabilir.

## Güvenlik ve yasaklar

- Açık onay olmadan kodlama veya UI değişikliği yapılmaz.
- 01–09’a dokunulmaz.
- 10–17 kabul edilmiş sayılmaz.
- Paper/live açılmaz.
- `LIVE_TRADING=true` oluşturulmaz.
- Gerçek emir veya Binance order endpoint eklenmez.
- Açık onay olmadan snapshot, test veya commit yapılmaz.
- Recovery, config, locked decisions ve anayasa değiştirilmez.

Mevcut güvenlik durumu: Paper `OFF`, Live `OFF / LOCKED`, `LIVE_TRADING=false`, `live_order_sending_allowed=false`, gerçek emir endpoint’i yoktur.

## STOP_AND_REPORT tetikleyicileri

Eksik veya çelişkili recovery kaydı, doğrulanamayan canonical dosya, hash/snapshot uyuşmazlığı, faz sırası ihlali, kapsam aşımı, kilitli karar değişikliği, açık mum kararı, ledger/PnL uyumsuzluğu, paper/live güvenlik riski veya gerçek emir endpoint’i şüphesi ilerlemeyi durdurur.

## Roller

- **User:** Kapsamı ve görsel/işlevsel kabulü onaylar; paper/live geçişleri için açık yetki verir.
- **ChatGPT:** Durumu okur, planı açıklar, riskleri ve gate sonuçlarını raporlar.
- **Codex:** Yalnız açıkça onaylanan kapsamı uygular; değişiklikleri sınırlar, doğrular ve raporlar.

Bu README yeni mimari, strateji veya kilitli karar oluşturmaz; yalnız proje açılış ve güvenli çalışma standardını özetler.
