# Tilson T3 — Recovery Rules

Durum: KİLİTLİ. Kaynak: `recovery/word/Tilson_T3_06_Recovery_Rules_Kilitli.docx`.

- Resmi okuma sırası ve recovery belgeleri olmadan işe başlanmaz.
- START/EXIT Gate 10/10 PASS şarttır; 9/10 FAIL’dir.
- Riskli değişikliklerden önce PRE-SNAPSHOT, sonrasında POST-SNAPSHOT alınır.
- UTF-8 bozulması, belirsizlik, açık mum kararı, ledger tutarsızlığı, live-lock şüphesi veya gate başarısızlığı `STOP_AND_REPORT` tetikler.
- Recovery, current state, phase tracker, changelog ve session handoff güncel tutulur.
- Kilitli Word dosyaları değiştirilmez.
