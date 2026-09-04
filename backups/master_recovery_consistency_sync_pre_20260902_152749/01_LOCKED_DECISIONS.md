# Tilson T3 — Kilitli Kararlar

Durum: KİLİTLİ. Kaynak: `recovery/word/Tilson_T3_01_Kilitli_Kararlar_KONU_1_48.docx`.

KONU-1 → KONU-48 kapalı ve kilitlidir. Özet ilkeler:

- TradingView uyumlu Tilson T3: factor 0.7, period 4, source `close`.
- DMI/ADX TradingView mantığı: DI length 24, ADX smoothing 24, varsayılan eşik 30.
- ADX slope varsayılanı 6 kapanmış 1H mumdur.
- Varsayılan giriş yalnızca T3 renk dönüşüdür; continuation OFF’tur.
- Aynı sembolde hedge yoktur; tek yönlü pozisyon vardır.
- Başlangıç wallet 1000 USD, varsayılan max coin 10, leverage 1x, isolated margin.
- Stop loss varsayılanı %2’dir; yeni ayar mevcut pozisyonlara geriye dönük uygulanmaz.
- Paper trading komisyon, funding ve slippage maliyetlerini izler.
- Panic > manual close > stop loss > T3 exit > continuation önceliği geçerlidir.
- Ledger tek resmi muhasebe kaynağıdır; live işlem ayrı Live Gate olmadan açılamaz.

Değişiklik protokolü: eski karar korunur, yeni konu/karar açılır.

## KONU-49 — Excel `.xlsx` export kütüphanesi

- Durum: **LOCKED**
- Onay: Kullanıcı onayladı.
- Kütüphane: `openpyxl`
- Kullanım alanı: Yalnız Faz-14 Report / Excel Export.
- Sebep: `@oai/artifact-tool` Codex ortamında mevcut değil.
- Ledger otoritesi: Değişmez; tek kaynak Ledger’dır.
- Live: Kapalı kalır.
- `LIVE_TRADING=true`: Yasak.

## KONU-50 — UI Operasyon Merkezi, Paper Çalıştırma ve Live’a Kontrollü Geçiş Kararı

- Durum: LOCKED.
- Faz-0 → Faz-20 tamamlanmadan doğrudan paper/live veya plansız kod geliştirme yoktur.
- UI, paper start öncesi tam operasyon merkezi olarak doğrulanır; UI functional PASS olmadan paper trade başlatılamaz.
- Paper stability PASS olmadan Live Readiness Audit’e geçilmez; Live Gate olmadan gerçek emir yoktur.
- Ledger tek kaynak, Recovery Gate ve STOP_AND_REPORT her aşamada geçerlidir.
