# Tilson T3 Projesi — Proje Anayasası

Durum: KİLİTLİ. Kaynak: `recovery/word/Tilson_T3_00_Proje_Anayasasi_Kilitli.docx`.

- Recovery, kilitli kararlar, faz akışı ve layer mimarisi dışında ilerleme yoktur.
- START GATE ve EXIT GATE 10/10 PASS olmalıdır; 9/10 veya altı FAIL’dir.
- Belirsizlikte `STOP_AND_REPORT` uygulanır.
- Başlangıç modu Paper Only’dir; live işlem kilitlidir ve varsayılan `LIVE_TRADING=false`’dır.
- Kararlar yalnızca kapanmış 1H mumdan üretilir; sinyal işlem değildir.
- Ledger tek muhasebe kaynağıdır.
- Kilitli karar doğrudan değiştirilemez; yeni karar açılır, eskisi gerekirse `SUPERSEDED` olur.
- Faz atlama, test/snapshot/recovery atlama ve onaysız Codex işi yasaktır.

Faz-0 kapsamı yalnızca proje koruma, recovery ve dokümantasyon başlangıç iskeletidir.
