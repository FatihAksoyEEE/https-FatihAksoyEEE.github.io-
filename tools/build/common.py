"""Ortak parçalar: head, header, footer, iki dilli metin ve diyagram yardımcıları."""
import html

SITE = "https://fatihaksoy.com"
UPDATED = ("Ekim 2026", "October 2026")


def b(tr, en):
    """Satır içi iki dilli metin."""
    return f'<span data-lang="tr">{tr}</span><span data-lang="en" lang="en">{en}</span>'


def B(tag, tr, en, attrs=""):
    """Blok düzeyinde iki dilli eleman (p, li, h2...)."""
    a = f" {attrs}" if attrs else ""
    return f'<{tag} data-lang="tr"{a}>{tr}</{tag}>\n<{tag} data-lang="en" lang="en"{a}>{en}</{tag}>'


def head(title_tr, title_en, desc_tr, path, og_image="assets/og.jpg", og_type="website"):
    url = f"{SITE}/{path}" if path else f"{SITE}/"
    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{e(title_tr)}</title>
    <meta name="title-en" content="{e(title_en)}">
    <meta name="description" content="{e(desc_tr)}">
    <meta name="author" content="Fatih Aksoy">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="Fatih Aksoy">
    <meta property="og:title" content="{e(title_tr)}">
    <meta property="og:description" content="{e(desc_tr)}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SITE}/{og_image}">
    <meta property="og:locale" content="tr_TR">
    <meta property="og:locale:alternate" content="en_US">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="theme-color" content="#f3f0e8" media="(prefers-color-scheme: light)">
    <meta name="theme-color" content="#161718" media="(prefers-color-scheme: dark)">
    <link rel="icon" href="favicon.svg" type="image/svg+xml">
    <link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
    <link rel="apple-touch-icon" href="apple-touch-icon.png">
    <script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;var l=localStorage.getItem('lang');if(l==='en')document.documentElement.lang='en'}}catch(e){{}}</script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
"""


THEME_ICONS = """<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
                <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 1.5v2.5M12 20v2.5M4.6 4.6l1.8 1.8M17.6 17.6l1.8 1.8M1.5 12H4M20 12h2.5M4.6 19.4l1.8-1.8M17.6 6.4l1.8-1.8"/></svg>"""


def header(on_home=True, active=None):
    pre = "" if on_home else "index.html"
    def item(anchor, tr, en):
        cur = ' aria-current="page"' if active == anchor else ""
        return f'<li><a href="{pre}#{anchor}"{cur}>{b(tr, en)}</a></li>'
    return f"""<body>
    <a class="skip-link" href="#main">{b("İçeriğe geç", "Skip to content")}</a>
    <header class="site-header">
        <div class="wrap">
            <a class="brand" href="{'#top' if on_home else 'index.html'}">Fatih Aksoy <span class="label">EEE</span></a>
            <nav class="site-nav" aria-label="{'Ana menü'}">
                <ul>
                    {item("about", "Hakkında", "About")}
                    {item("projects", "Projeler", "Projects")}
                    {item("contact", "İletişim", "Contact")}
                </ul>
            </nav>
            <div class="controls">
                <button class="ctrl-btn" id="langBtn" type="button" lang="en" aria-label="Switch to English">EN</button>
                <button class="ctrl-btn" id="themeBtn" type="button" aria-label="Temayı değiştir">
                {THEME_ICONS}
                </button>
            </div>
        </div>
    </header>
"""


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

class Diagram:
    _n = 0

    def __init__(self, w, h, title):
        Diagram._n += 1
        self.id = f"ah{Diagram._n}"
        self.w, self.h, self.title = w, h, title
        self.parts = []

    def box(self, x, y, w, h, t, s=None, accent=False):
        need = max(len(t) * 7.9, len(s or "") * 6.7) + 14
        if need > w:
            print(f"WARN {self.title}: '{t}'/'{s}' needs {need:.0f}px, box {w}px")
        cls = "blk-accent" if accent else "blk"
        self.parts.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/>')
        cy = y + h / 2 + (-3 if s else 4)
        self.parts.append(f'<text class="t" x="{x + w / 2}" y="{cy}" text-anchor="middle">{html.escape(t)}</text>')
        if s:
            self.parts.append(f'<text class="s" x="{x + w / 2}" y="{cy + 17}" text-anchor="middle">{html.escape(s)}</text>')
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
            self.parts.append(f'<text class="s" x="{lx}" y="{ly}" text-anchor="middle">{html.escape(label)}</text>')
        return self

    def text(self, x, y, t, cls="s", anchor="start"):
        self.parts.append(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{html.escape(t)}</text>')
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
        return (f'<div class="diagram"><svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{html.escape(self.title)}">'
                f'{defs}\n            {body}\n            </svg></div>')
