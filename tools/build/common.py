"""Ortak parçalar: head, header, footer, iki dilli metin ve diyagram yardımcıları."""
import html, json

SITE = "https://fatihaksoy.com"
UPDATED = ("Ekim 2026", "October 2026")
# GoatCounter site kodu (örn. "fatihaksoy" → fatihaksoy.goatcounter.com). Boş bırakılırsa sayaç eklenmez.
GOATCOUNTER = ""


def b(tr, en):
    """Satır içi iki dilli metin."""
    return f'<span data-lang="tr">{tr}</span><span data-lang="en" lang="en">{en}</span>'


def B(tag, tr, en, attrs=""):
    """Blok düzeyinde iki dilli eleman (p, li, h2...)."""
    a = f" {attrs}" if attrs else ""
    return f'<{tag} data-lang="tr"{a}>{tr}</{tag}>\n<{tag} data-lang="en" lang="en"{a}>{en}</{tag}>'


def page_url(path, lang):
    """Sayfanın mutlak adresi. Türkçe kökte, İngilizce /en/ altında."""
    return f"{SITE}/{'en/' if lang == 'en' else ''}{path}"


def head(title, desc, path, lang, og_image="assets/og.jpg", og_type="website", ld=None, noindex=False):
    e = html.escape
    url = page_url(path, lang)
    locale, alt = ("en_US", "tr_TR") if lang == "en" else ("tr_TR", "en_US")
    alternates = "" if noindex else (
        f'    <link rel="alternate" hreflang="tr" href="{page_url(path, "tr")}">\n'
        f'    <link rel="alternate" hreflang="en" href="{page_url(path, "en")}">\n'
        f'    <link rel="alternate" hreflang="x-default" href="{page_url(path, "tr")}">\n')
    robots = '    <meta name="robots" content="noindex">\n' if noindex else ""
    ld_tag = (f'    <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n') if ld else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">
    <meta name="author" content="Fatih Aksoy">
{robots}    <link rel="canonical" href="{url}">
{alternates}    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="Fatih Aksoy">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(desc)}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE}/{og_image}">
    <meta property="og:locale" content="{locale}">
    <meta property="og:locale:alternate" content="{alt}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="theme-color" content="#f3f0e8" media="(prefers-color-scheme: light)">
    <meta name="theme-color" content="#161718" media="(prefers-color-scheme: dark)">
    <link rel="icon" href="favicon.svg" type="image/svg+xml">
    <link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
    <link rel="preload" href="assets/fonts/ibm-plex-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="styles.css">
{analytics()}{ld_tag}</head>
"""


def analytics():
    """GoatCounter: çerezsiz ziyaret sayacı. GOATCOUNTER boşsa hiçbir şey eklenmez."""
    if not GOATCOUNTER:
        return ""
    return (f'    <script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" '
            f'async src="https://gc.zgo.at/count.js"></script>\n')


THEME_ICONS = """<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
                <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 1.5v2.5M12 20v2.5M4.6 4.6l1.8 1.8M17.6 17.6l1.8 1.8M1.5 12H4M20 12h2.5M4.6 19.4l1.8-1.8M17.6 6.4l1.8-1.8"/></svg>"""


def header(lang, path, on_home=True, active=None):
    pre = "" if on_home else "index.html"
    def item(anchor, tr, en):
        cur = ' aria-current="page"' if active == anchor else ""
        return f'<li><a href="{pre}#{anchor}"{cur}>{b(tr, en)}</a></li>'
    return f"""<body>
    <a class="skip-link" href="#main">{b("İçeriğe geç", "Skip to content")}</a>
    <header class="site-header">
        <div class="wrap">
            <a class="brand" href="{'#top' if on_home else 'index.html'}">Fatih Aksoy <span class="label">EEE</span></a>
            <nav class="site-nav" aria-label="{'Main menu' if lang == 'en' else 'Ana menü'}">
                <ul>
                    {item("about", "Hakkında", "About")}
                    {item("projects", "Projeler", "Projects")}
                    {item("contact", "İletişim", "Contact")}
                </ul>
            </nav>
            <div class="controls">
                {lang_switch(lang, path)}
                <button class="ctrl-btn" id="themeBtn" type="button" aria-label="{'Toggle theme' if lang == 'en' else 'Temayı değiştir'}">
                {THEME_ICONS}
                </button>
            </div>
        </div>
    </header>
"""


def lang_switch(lang, path):
    # Erişilebilir ad görünen metinle aynı kalsın diye aria-label yok; açıklama title'da
    if lang == "en":
        return f'<a class="ctrl-btn" id="langBtn" href="../{path}" hreflang="tr" lang="tr" title="Türkçe">TR</a>'
    return f'<a class="ctrl-btn" id="langBtn" href="en/{path}" hreflang="en" lang="en" title="English">EN</a>'


def footer():
    return f"""    <footer class="site-footer">
        <div class="wrap">
            <span class="label">© 2026 Fatih Aksoy</span>
            <span class="label">{b("Son güncelleme: " + UPDATED[0], "Last updated: " + UPDATED[1])}</span>
            <a class="label" href="https://github.com/FatihAksoyEEE/https-FatihAksoyEEE.github.io-">{b("Sitenin kaynağı", "Site source")} ↗</a>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>
"""


# ---------- SVG blok diyagram yardımcıları ----------

# Diyagram etiketlerinin İngilizcesi. Listede olmayan etiketler (parça adları, pinler) iki dilde aynıdır.
DIAGRAM_EN = {
    "0x2C4 çerçevesinin bayt yerleşimi": "Byte layout of frame 0x2C4",
    "12 V · motorlar": "12 V · motors",
    "12–36 V giriş": "12–36 V input",
    "1S Li-Po şarj": "1S Li-Po charger",
    "3 × step sürücü": "3 × step driver",
    "5 V · lojik": "5 V · logic",
    "Araç ECU'ları": "Vehicle ECUs",
    "CAN ID 0x2C4 · DLC 8 · örnek çerçeve": "CAN ID 0x2C4 · DLC 8 · sample frame",
    "CAN dinleme zinciri blok diyagramı": "CAN sniffing chain block diagram",
    "CNC kontrol kartı blok diyagramı": "CNC controller board block diagram",
    "D2–D7: bu çalışmada kullanılmadı": "D2–D7: not used in this work",
    "DigiTab mimari diyagramı": "DigiTab architecture diagram",
    "ESP32 quadcopter kartı blok diyagramı": "ESP32 quadcopter board block diagram",
    "Fiş yazıcısı": "Ticket printer",
    "Garson telefonu": "Waiter phone",
    "Görev planlayıcı": "Mission planner",
    "Kasa bilgisayarı": "Cashier computer",
    "Arayüz / CLI": "GUI / CLI",
    "Dışa aktarma": "Export",
    "Kanal": "Channel",
    "LoRaSim mimari diyagramı": "LoRaSim architecture diagram",
    "Metrikler": "Metrics",
    "Olay zamanlayıcı": "Event scheduler",
    "PHY modeli": "PHY model",
    "PER · RSSI · enerji": "PER · RSSI · energy",
    "Vericiler": "Transmitters",
    "doğrulama · JSON": "validation · JSON",
    "heapq · tek seed": "heapq · single seed",
    "kayıp · sönümleme": "loss · fading",
    "kayıt": "records",
    "paket": "packet",
    "trafik · ACK · DC": "traffic · ACK · DC",
    "OBD-II soketi": "OBD-II port",
    "PFD + telemetri": "PFD + telemetry",
    "Paket ayrıştırıcı": "Packet parser",
    "PyQt6 arayüz": "PyQt6 GUI",
    "Robot kol kontrol sistemi blok diyagramı": "Robot arm control system block diagram",
    "Step motorlar": "Stepper motors",
    "Telsiz / seri": "Radio / serial",
    "Yer kontrol istasyonu blok diyagramı": "Ground control station block diagram",
    "batarya gerilimi": "battery voltage",
    "bilgisayar · USB": "computer · USB",
    "devir saati": "tachometer",
    "fiş · hazır": "tickets · ready",
    "fırçalı motor": "brushed motor",
    "görev": "mission",
    "kalibrasyon": "calibration",
    "kontrol üniteleri": "control units",
    "servo gücü": "servo power",
    "sipariş": "orders",
    "tablet · mutfak": "tablet · kitchen",
    "tarayıcı · QR kod": "browser · QR code",
    "tek dosya · yerel": "single local file",
    "telemetri": "telemetry",
    "ufuk · şeritler": "horizon · tapes",
    "uçuş kontrolcüsü": "flight controller",
    "yazdır": "print",
    "çerçeve → CSV": "frames → CSV",
    "İHA": "UAV",
    "İstasyon ekranı": "Station screen",
}


def dt(t):
    """Diyagram metni: çevirisi varsa iki dilli <tspan> çifti, yoksa düz metin."""
    en = DIAGRAM_EN.get(t)
    if en is None:
        return html.escape(t)
    return f'<tspan data-lang="tr">{html.escape(t)}</tspan><tspan data-lang="en" lang="en">{html.escape(en)}</tspan>'

class Diagram:
    _n = 0

    def __init__(self, w, h, title):
        Diagram._n += 1
        self.id = f"ah{Diagram._n}"
        self.w, self.h, self.title = w, h, title
        self.parts = []

    def box(self, x, y, w, h, t, s=None, accent=False):
        L = lambda x: max(len(x), len(DIAGRAM_EN.get(x, x)))
        need = max(L(t) * 7.9, L(s or "") * 6.7) + 14
        if need > w:
            print(f"WARN {self.title}: '{t}'/'{s}' needs {need:.0f}px, box {w}px")
        cls = "blk-accent" if accent else "blk"
        self.parts.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/>')
        cy = y + h / 2 + (-3 if s else 4)
        self.parts.append(f'<text class="t" x="{x + w / 2}" y="{cy}" text-anchor="middle">{dt(t)}</text>')
        if s:
            self.parts.append(f'<text class="s" x="{x + w / 2}" y="{cy + 17}" text-anchor="middle">{dt(s)}</text>')
        return self

    def wire(self, pts, label=None, lx=None, ly=None, arrow=True, both=False):
        d = " ".join(f"{x},{y}" for x, y in pts)
        m = f' marker-end="url(#{self.id})"' if arrow else ""
        if both:
            m += f' marker-start="url(#{self.id}s)"'
        self.parts.append(f'<polyline class="wire" points="{d}"{m}/>')
        if label:
            if lx is None:
                (x1, y1), (x2, y2) = pts[0], pts[-1]
                lx, ly = (x1 + x2) / 2, (y1 + y2) / 2 - 7
            self.parts.append(f'<text class="s" x="{lx}" y="{ly}" text-anchor="middle">{dt(label)}</text>')
        return self

    def text(self, x, y, t, cls="s", anchor="start"):
        self.parts.append(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{dt(t)}</text>')
        return self

    def raw(self, s):
        self.parts.append(s)
        return self

    def render(self):
        defs = (f'<defs><marker id="{self.id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                f'<path class="arrowhead" d="M0,1 L9,5 L0,9 z"/></marker>'
                f'<marker id="{self.id}s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                f'<path class="arrowhead" d="M10,1 L1,5 L10,9 z"/></marker></defs>')
        body = "\n            ".join(self.parts)
        en = DIAGRAM_EN.get(self.title, self.title)
        titles = (f'<title data-lang="tr">{html.escape(self.title)}</title>'
                  f'<title data-lang="en" lang="en">{html.escape(en)}</title>')
        return (f'<div class="diagram"><svg viewBox="0 0 {self.w} {self.h}" role="img">{titles}'
                f'{defs}\n            {body}\n            </svg></div>')
