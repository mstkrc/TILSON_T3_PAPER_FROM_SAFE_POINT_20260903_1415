# Tilson T3 — Faz Bazlı İş Akışı

Durum: KİLİTLİ. Kaynak: `recovery/word/Tilson_T3_02_Faz_Bazli_Is_Akisi_Kilitli.docx`.

- Proje faz bazlı ilerler; her görev aktif faza bağlıdır.
- Faz başlangıcında START GATE, sonunda EXIT GATE uygulanır.
- Her fazda kapsam, yapılmayacaklar, bağlı layerlar, testler, snapshotlar ve handoff izlenir.
- 10/10 PASS olmadan sonraki faza geçilmez.
- Faz atlama, layer atlama, testsiz veya snapshotsız geçiş yasaktır.
- Faz-0: Recovery/UTF-8/dokümantasyon temelinin kurulması.
- Faz-1 ve sonrası başlangıçta `NOT_STARTED` durumundadır.
