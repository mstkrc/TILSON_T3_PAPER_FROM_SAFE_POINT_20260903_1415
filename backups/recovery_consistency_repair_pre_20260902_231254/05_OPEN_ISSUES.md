# Tilson T3 — Open Issues

## Güncel açık konular — Faz-21→47

- Grup-2 / 06–09: IMPLEMENTED / USER_QA_PENDING; kullanıcı görsel QA bekleniyor.
- Grup-2 kabul edilirse PASS kaydı yapılacaktır; mevcut kayıtta PASS_RECORDED değildir.
- Grup-3 / 10–13: PENDING.
- Grup-4 / 14–17: PENDING.
- Data binding: NOT_DONE.
- Paper: OFF. Live: OFF / LOCKED.
- Word/DOCX render QA gerekiyorsa ayrı kullanıcı onayı ve desteklenen render ortamı gerekir.

Kaynak: `recovery/word/Tilson_T3_05_Open_Issues_Kilitli.docx`.

**KONU-1 → KONU-50 kilitli; kritik açık issue yok.**

Yeni belirsizlik veya çelişki çıkarsa ilerleme durdurulur, konu açılır ve `STOP_AND_REPORT` uygulanır.

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
