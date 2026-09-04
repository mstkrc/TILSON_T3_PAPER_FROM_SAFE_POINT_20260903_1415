# Tilson T3 — Open Issues

## GÜN SONU KAPANIŞ — 2026-09-03

- 10–17 mevcut HTML çıktıları yalnız `UNACCEPTED_WORKING_ARTIFACTS` olarak tutulur; PASS, APPROVED, LOCKED veya BASELINE_PROTECTED değildir.
- 10–17 için `NOT_ACCEPTED / REWORK_PENDING / USER_LATER_QA_REQUIRED` ve ileride kullanıcı browser/manual QA şartı geçerlidir.
- Safe point `REVERTED_TO_GROUP2_APPROVED_STATE` olarak korunur; 01–09 `DO_NOT_TOUCH` kapsamındadır.

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
