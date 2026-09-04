"""06_GRAFIKLER display-only market chart screen."""

from ..components import action_stack, display_button, kv_list, line_chart, panel, table
from ..layout import render_screen


def _market_chart() -> str:
    candles = "".join(f'<i class="candle {"up" if i % 3 else "down"}" style="left:{i*3.2+2}%;height:{28+(i*17)%96}px;bottom:{70+(i*11)%115}px"></i>' for i in range(29))
    volume = "".join(f'<i class="volume {"up" if i % 3 else "down"}" style="left:{i*3.2+2}%;height:{12+(i*13)%38}px"></i>' for i in range(29))
    return f'<div class="market-chart"><div class="chart-toolbar">{display_button("BTC/USDT", "info", True)}{display_button("1H", "neutral")}{display_button("GÖSTERGELER", "neutral")}{display_button("AYARLAR", "neutral")}</div><div class="drawing-tools">＋<br>⌁<br>╱<br>□<br>◉<br>⌕</div><div class="price-stage">{candles}<svg viewBox="0 0 1000 300" preserveAspectRatio="none"><polyline points="0,210 80,195 160,220 240,175 320,190 400,140 480,155 560,110 640,128 720,75 800,102 900,58 1000,78" fill="none" stroke="#dfc15d" stroke-width="4"/></svg><span class="buy-marker">B</span><span class="sell-marker">S</span></div><div class="volume-stage">{volume}</div></div>'


def render_charts_screen(model=None) -> str:
    chart = panel("BTC/USDT · PERPETUAL", _market_chart() + line_chart(((19, 23, 27, 31, 29, 37, 42, 39, 46), (31, 29, 25, 22, 24, 19, 17, 20, 16), (18, 20, 22, 25, 28, 31, 34, 37, 40)), ("#41c77d", "#df6161", "#d7b956"), ("+DI", "-DI", "ADX")), "fill", "T3 · HACİM · DMI / ADX · ADX SLOPE")
    coin = panel("SEÇİLİ COİN", kv_list((("Sembol", "BTC/USDT"), ("Fiyat", "68,302.54"), ("24s", "+2.18%"), ("Hacim", "2.23B"), ("Candle", "CLOSED"))), "compact")
    strategy = panel("STRATEJİ ÖZETİ", kv_list((("T3", "YEŞİL / DEVAM"), ("DMI", "+DI 36.7"), ("ADX", "35.7"), ("Slope", "UP"), ("Final", "LONG / PASS"))), "compact")
    position = panel("AÇIK POZİSYON", kv_list((("Yön", "LONG"), ("Giriş", "68,200.00"), ("Net PnL", "+102.54"), ("Stop", "ON / %2"), ("Aksiyon", "DISPLAY ONLY"))), "compact")
    bottom = '<div class="screen-grid grid-3 lower-row">' + panel("ZAMAN ARALIĞI / ARAÇLAR", action_stack((("1M", "neutral"), ("5M", "neutral"), ("15M", "neutral"), ("1H · AKTİF", "info"), ("4H", "neutral"))), "compact") + panel("GÖSTERGE DEĞERLERİ", table(("Gösterge", "Değer", "Durum"), (("T3", "68,122.4", "YEŞİL"), ("+DI", "36.7", "PASS"), ("-DI", "12.6", "PASS"), ("ADX", "35.7", "UP")), "dense"), "compact") + panel("HIZLI NOTLAR", kv_list((("19:42", "Closed candle PASS"), ("19:41", "Rank 1 / Risk PASS"), ("19:40", "Live locked"))), "compact") + '</div>'
    body = f'<div class="screen-grid with-rail fill"><div class="stack fill">{chart}{bottom}</div><aside class="stack fill">{coin}{strategy}{position}</aside></div>'
    return render_screen("GRAFİKLER", "Grafikler", body, "Trading görünümü · göstergeler display-only", "charts-screen")
