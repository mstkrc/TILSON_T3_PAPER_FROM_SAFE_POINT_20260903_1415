# Tilson T3 — Open Issues

## UI Control Center render riski

UI model/intent altyapısı hazırlandı; gerçek frontend/render QA ayrı kullanıcı onayı ve desteklenen render ortamı gerektirir. Bu kayıt UI model kapsamındadır; paper/live işlem başlatmaz.

Kaynak: `recovery/word/Tilson_T3_05_Open_Issues_Kilitli.docx`.

**Açık konu yok; KONU-1 → KONU-48 kilitli.**

Yeni belirsizlik veya çelişki çıkarsa ilerleme durdurulur, konu açılır ve `STOP_AND_REPORT` uygulanır.

## Faz-14 blocker

- `@oai/artifact-tool` çalışma ortamında mevcut değil.
- `.xlsx` export oluşturma/doğrulaması yapılamıyor.
- Report modeli, filtreler, Ledger kaynak kontrolü ve Excel export uygulanmadı.
- Durum: **Çözüldü — KONU-49 ile Faz-14 için `openpyxl` onaylandı.**
- openpyxl 3.1.5 doğrulandı; eski artifact-tool blocker tarihsel kayıt olarak korunur.
- Kritik açık issue yok.

KONU-50: LOCKED. Faz-21 → Faz-47 planı kayıtlıdır; tüm sonraki fazlar NOT_STARTED ve kullanıcı onayı gerektirir. Kritik açık issue yok.
- Artifact-tool blocker: çözüldü; openpyxl 3.1.5 doğrulandı.
- Word/DOC final paket güncellemesi kullanıcı onaylı sonraki çalışma olarak bekliyor.
- Render QA blocker: pdf2image ve LibreOffice/soffice mevcut değil.
- Çözüm: Render destekli ortam sağlandığında 12 DOCX için görsel QA yeniden çalıştırılacak.
- Render QA durumu: BLOCKED / WAITING_RENDER_ENV.
- Faz-14 export doğrulaması tamamlandı; blocker kapalı, Faz-14 PASS / LOCKED.
