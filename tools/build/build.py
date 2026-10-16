"""Sitenin HTML sayfalarını üretir: python3 tools/build/build.py

index.html, project-*.html, en/ altındaki İngilizce kopyaları, 404.html, sitemap.xml ve robots.txt
bu betikle üretilir. Metinler iki dilli yazılır (b/B); her dil için diğer dilin elemanları çıkarılır. Header/footer gibi
ortak parçalar common.py, proje içerikleri projects.py içindedir. Gereksinim: Pillow (görsel boyutları için).
"""
import os, re, sys, html
from html.parser import HTMLParser
from PIL import Image
from common import b, B, head, header, footer, page_url, SITE, UPDATED
from projects import PROJECTS

# Varsayılan: repo kökü (tools/build/../..)
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMG = "assets/img/"


def size(path):
    if path.endswith(".svg"):
        with open(os.path.join(ROOT, path)) as f:
            m = re.search(r'<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"', f.read())
        return int(m.group(1)), int(m.group(2))
    with Image.open(os.path.join(ROOT, path)) as im:
        return im.size


def img(path, alt, cls="", lazy=True, extra=""):
    w, h = size(IMG + path)
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="{IMG}{path}" width="{w}" height="{h}" alt="{html.escape(alt)}"{c}{l}{extra}>'


def expand_figs(s, counter, lang):
    en = lang == "en"
    def rep(m):
        path, t_tr, t_en, c_tr, c_en, cls = m.group(1).split("|")
        counter[0] += 1
        n = counter[0]
        t, c = (t_en, c_en) if en else (t_tr, c_tr)
        alt = t + (f": {c}" if c else "")
        cap = b(f"Şekil {n}", f"Fig. {n}")
        text = b(t_tr + (f" — {c_tr}" if c_tr else ""), t_en + (f" — {c_en}" if c_en else ""))
        return (f'<figure class="fig"><a href="{IMG}{path}">{img(path, alt, cls)}</a>'
                f'<figcaption><span class="label">{cap}</span>{text}</figcaption></figure>')
    def rep_vid(m):
        # {vid:video.mp4|poster.webp|Başlık|Title|açıklama|caption}
        path, poster, t_tr, t_en, c_tr, c_en = m.group(1).split("|")
        counter[0] += 1
        n = counter[0]
        w, h = size(IMG + poster)
        cap = b(f"Şekil {n}", f"Fig. {n}")
        text = b(t_tr + (f" — {c_tr}" if c_tr else ""), t_en + (f" — {c_en}" if c_en else ""))
        return (f'<figure class="fig"><video controls muted playsinline preload="none" '
                f'poster="{IMG}{poster}" width="{w}" height="{h}" aria-label="{html.escape(t_en if en else t_tr)}">'
                f'<source src="{IMG}{path}" type="video/mp4"></video>'
                f'<figcaption><span class="label">{cap}</span>{text}</figcaption></figure>')
    s = re.sub(r"\{vid:([^}]*)\}", rep_vid, s)
    return re.sub(r"\{fig:([^}]*)\}", rep, s)


def label(l):
    return b(*l) if isinstance(l, tuple) else l


# ---------------------------------------------------------------------------
def project_page(i, p, lang):
    num = f"{i + 1:02d}"
    t_tr, t_en = p["title"]
    L = 1 if lang == "en" else 0
    og = IMG + (p.get("og") or p["thumb"][0]) if p.get("thumb") else "assets/og.jpg"
    ld = {"@context": "https://schema.org", "@type": "CreativeWork",
          "name": p["title"][L], "description": p["desc"][L], "url": page_url(p["slug"], lang),
          "image": f"{SITE}/{og}", "dateCreated": p["year"], "inLanguage": lang,
          "keywords": p["tags_en" if L else "tags"].replace(" · ", ", "),
          "author": {"@id": f"{SITE}/#person"}}
    out = head(f"{p['title'][L]} · Fatih Aksoy", p["desc"][L], p["slug"], lang,
               og_image=og, og_type="article", ld=ld)
    out += header(lang, p["slug"], on_home=False, active="projects")
    meta = "\n".join(f'<div><dt class="label">{label(k)}</dt><dd>{v}</dd></div>' for k, v in p["meta"])
    counter = [0]
    toc, secs = [], []
    for j, (sid, (h_tr, h_en), body) in enumerate(p["sections"]):
        n = f"{j + 1}"
        toc.append(f'<li><a href="#{sid}"><span class="n">{n}</span>{b(h_tr, h_en)}</a></li>')
        secs.append(f'<section class="ds-section" id="{sid}" aria-labelledby="{sid}-h">\n'
                    f'<h2 id="{sid}-h"><span class="num">{num}.{n}</span>{b(h_tr, h_en)}</h2>\n'
                    f'{expand_figs(body, counter, lang)}\n</section>')
    prev_p = PROJECTS[i - 1] if i > 0 else None
    next_p = PROJECTS[i + 1] if i + 1 < len(PROJECTS) else None
    pager = '<nav class="pager wrap" aria-label="' + ("Project navigation" if L else "Proje gezinme") + '">'
    pager += (f'<a href="{prev_p["slug"]}"><span class="label">← {b("Önceki", "Previous")}</span><strong>{b(*prev_p["short"])}</strong></a>'
              if prev_p else '<span></span>')
    pager += (f'<a href="{next_p["slug"]}"><span class="label">{b("Sonraki", "Next")} →</span><strong>{b(*next_p["short"])}</strong></a>'
              if next_p else '<span></span>')
    pager += "</nav>"
    out += f"""
    <main id="main">
        <div class="wrap">
            <a class="crumb" href="index.html#projects">← {b("Tüm projeler", "All projects")}</a>
            <header class="ds-head">
                <p class="label">{b("Proje", "Project")} {num} · {p["year"]}</p>
                <h1>{b(t_tr, t_en)}</h1>
                {B("p", p["desc"][0], p["desc"][1], 'class="lead"')}
                <dl class="ds-meta">
{meta}
                </dl>
            </header>
            <div class="ds-body">
                <nav class="ds-toc" aria-label="{"Contents" if L else "İçindekiler"}">
                    <p class="label">{b("İçindekiler", "Contents")}</p>
                    <ol>{''.join(toc)}</ol>
                </nav>
                <div class="ds-content">
{chr(10).join(secs)}
                </div>
            </div>
        </div>
        {pager}
    </main>
"""
    out += footer()
    return out


# ---------------------------------------------------------------------------
CATS = [("pcb", "PCB", "PCB"), ("fw", "Firmware", "Firmware"), ("sw", "Yazılım", "Software")]

PERSON = {
    "@context": "https://schema.org", "@type": "Person", "@id": f"{SITE}/#person",
    "name": "Mehmet Fatih Aksoy", "alternateName": "Fatih Aksoy", "url": f"{SITE}/",
    "image": f"{SITE}/assets/img/portrait.webp",
    "jobTitle": "Electrical and Electronics Engineering Student",
    "affiliation": {"@type": "CollegeOrUniversity", "name": "Zonguldak Bülent Ecevit Üniversitesi"},
    "knowsAbout": ["Embedded systems", "PCB design", "STM32", "ESP32", "KiCad", "CAN bus", "Industrial automation", "PLC"],
    "sameAs": ["https://github.com/FatihAksoyEEE",
               "https://www.linkedin.com/in/mehmet-fatih-aksoy-1217443ba",
               "https://www.youtube.com/@electronc_workshop",
               "https://www.instagram.com/fatih_aksoy6741/"],
}


def index_page(lang):
    L = 1 if lang == "en" else 0
    out = head(("Fatih Aksoy · Elektrik-Elektronik Mühendisliği", "Fatih Aksoy · Electrical & Electronics Engineering")[L],
               ("Fatih Aksoy: gömülü sistemler, PCB tasarımı ve otomasyon üzerine çalışan elektrik-elektronik mühendisliği öğrencisi. Projeler, şemalar ve kaynak kodlar.",
                "Fatih Aksoy: electrical and electronics engineering student working on embedded systems, PCB design and automation. Projects, schematics and source code.")[L],
               "", lang, ld=PERSON)
    out += header(lang, "", on_home=True)
    counts = {c: sum(c in p["cats"] for p in PROJECTS) for c, _, _ in CATS}
    filt = (f'<div class="filter" role="group" aria-label="{("Projeleri filtrele", "Filter projects")[L]}" hidden>'
            f'<button type="button" aria-pressed="true" data-cat="">{b("Tümü", "All")} <span class="n">{len(PROJECTS)}</span></button>'
            + "".join(f'<button type="button" aria-pressed="false" data-cat="{c}">{b(tr, en)} <span class="n">{counts[c]}</span></button>'
                      for c, tr, en in CATS)
            + "</div>")
    rows = []
    for i, p in enumerate(PROJECTS):
        if p.get("thumb"):
            thumb = img(p["thumb"][0], "", "thumb").replace('alt=""', 'alt="" aria-hidden="true"')
        else:
            thumb = f'<span class="thumb thumb-text" aria-hidden="true">{html.escape(p["thumb_text"])}</span>'
        rows.append(f"""<li data-cats="{' '.join(p['cats'])}"><a class="project-row" href="{p['slug']}">
    <span class="idx">{i + 1:02d}</span>
    <div class="body"><h3>{b(*p['short'])}</h3>{B("p", p['desc'][0], p['desc'][1], 'class="desc"')}</div>
    <div class="meta"><span>{p['year']}</span><span>{b(p['tags'], p['tags_en'])}</span></div>
    {thumb}
</a></li>""")
    portrait = ('<img src="assets/img/portrait.webp" srcset="assets/img/portrait-480.webp 480w, assets/img/portrait.webp 900w" '
                'sizes="(min-width: 860px) 420px, 90vw" width="900" height="958" alt="Fatih Aksoy\'nun karakalem portresi" fetchpriority="high">')
    out += f"""
    <main id="main">
        <section class="hero" id="top">
            <div class="wrap">
                <div>
                    <p class="label">{b("Elektrik-elektronik mühendisliği · 4. sınıf", "Electrical &amp; electronics engineering · 4th year")}</p>
                    <h1>Fatih Aksoy</h1>
                    {B("p", "Gömülü sistemler, PCB tasarımı ve otomasyon üzerine çalışıyorum. Kartı tasarlamaktan firmware'ini ve onu kullanan masaüstü arayüzü yazmaya kadar projenin tamamını üstlenmeyi seviyorum.",
                       "I work on embedded systems, PCB design and automation. I like owning a project end to end: from designing the board to writing its firmware and the desktop app that drives it.", 'class="lead"')}
                    <div class="actions">
                        <a class="btn btn-primary" href="#projects">{b("Projeler", "Projects")} <span class="arrow">↓</span></a>
                        <a class="btn" href="assets/Mehmet_Fatih_Aksoy_CV_TR-EN.pdf" download="Mehmet_Fatih_Aksoy_CV.pdf" data-goatcounter-click="cv-indir">{b("CV indir", "Download CV")} <span class="arrow">PDF</span></a>
                        <a class="btn" href="https://github.com/FatihAksoyEEE">GitHub <span class="arrow">↗</span></a>
                    </div>
                </div>
                <figure class="hero-figure">
                    {portrait}
                </figure>
            </div>
        </section>

        <section class="section" id="about" aria-labelledby="about-h">
            <div class="wrap">
                <div class="section-head"><span class="num">01</span><h2 id="about-h">{b("Hakkında", "About")}</h2></div>
                <div class="about-grid">
                    <div>
                        {B("p", "Merhaba, ben Fatih. Zonguldak Bülent Ecevit Üniversitesi'nde elektrik-elektronik mühendisliği son sınıf öğrencisiyim. Kendimi en çok <strong>gömülü sistemler</strong>, <strong>PCB tasarımı</strong> ve <strong>otomasyon</strong> alanlarında, gerçek donanım üzerinde çalışarak geliştiriyorum.",
                           "Hi, I'm Fatih, a final-year electrical and electronics engineering student at Zonguldak Bülent Ecevit University. I learn best by working on real hardware, mostly in <strong>embedded systems</strong>, <strong>PCB design</strong> and <strong>automation</strong>.")}
                        {B("p", "Son projelerimde bir quadcopter'ın uçuş kartını KiCad'de çizdim, STM32 ile bir robot kolu sürdüm, bir aracın CAN hattını dinleyerek motor devri sinyalini tersine mühendislikle çözdüm ve bunlarla konuşan masaüstü arayüzleri yazdım.",
                           "Recently I drew a quadcopter flight board in KiCad, drove a robot arm with an STM32, reverse-engineered a vehicle's engine-speed signal by listening to its CAN bus, and wrote the desktop apps that talk to them.")}
                        {B("p", "Endüstriyel otomasyon ve iş makinesi haberleşmesi üzerine iki staj yaptım.",
                           "I have completed two internships, in industrial automation and in heavy-machinery communication systems.")}
                    </div>
                    <table class="spec">
                        <tr><th scope="row">{b("Odak", "Focus")}</th><td>{b("Gömülü yazılım, PCB tasarımı, haberleşme protokolleri, otomasyon", "Embedded software, PCB design, communication protocols, automation")}</td></tr>
                        <tr><th scope="row">MCU</th><td>STM32, ESP32, AVR (ATmega328P)</td></tr>
                        <tr><th scope="row">{b("Donanım", "Hardware")}</th><td>KiCad, Altium, Fusion 360, SolidWorks</td></tr>
                        <tr><th scope="row">{b("Yazılım", "Software")}</th><td>C/C++ (PlatformIO, Arduino), Python (PyQt6, python-can), JavaScript (React, Electron, Node.js)</td></tr>
                        <tr><th scope="row">{b("Protokoller", "Protocols")}</th><td>CAN, UART, I²C, SPI, USB-CDC, LoRa, ESP-NOW</td></tr>
                        <tr><th scope="row">{b("Otomasyon", "Automation")}</th><td>{b("Siemens ve Delta PLC, TIA Portal, motor sürücüleri, elektrik panoları", "Siemens and Delta PLCs, TIA Portal, motor drives, electrical panels")}</td></tr>
                        <tr><th scope="row">{b("Simülasyon", "Simulation")}</th><td>MATLAB, Simulink</td></tr>
                    </table>
                </div>
                <h3 class="label timeline-title">{b("Eğitim ve staj", "Education and internships")}</h3>
                <table class="spec timeline">
                    <tr><th scope="row">{b("2027 (beklenen)", "2027 (expected)")}</th><td><strong>{b("Lisans · Zonguldak Bülent Ecevit Üniversitesi", "B.Sc. · Zonguldak Bülent Ecevit University")}</strong><br>{b("Elektrik-Elektronik Mühendisliği", "Electrical and Electronics Engineering")}</td></tr>
                    <tr><th scope="row">{b("Haziran 2026", "June 2026")}</th><td><strong>{b("Stajyer · Sistem Vinç A.Ş.", "Intern · Sistem Vinç A.Ş.")}</strong><br>{b("Ağır iş makinelerindeki elektrik ve elektronik arızalara çözümler; CAN tabanlı sensör haberleşmesi, hidrolik ve pnömatik kontrol.", "Solutions for electrical and electronic faults in heavy machinery; CAN-based sensor communication, hydraulic and pneumatic control.")}</td></tr>
                    <tr><th scope="row">{b("Haziran–Temmuz 2024", "June–July 2024")}</th><td><strong>{b("Stajyer · Ensan, Otomasyon Bölümü", "Intern · Ensan, Automation Department")}</strong><br>{b("Endüstriyel otomasyon makinelerinin bakım ve onarımında Siemens ve Delta PLC'ler, motor sürücüleri ve elektrik panoları; sıfırdan makine üretiminin elektrik-elektronik tarafı; görüntü tabanlı hata tespit sistemleri.", "Siemens and Delta PLCs, motor drives and electrical panels in the maintenance of industrial automation machines; electrical work on machines built from scratch; vision-based fault detection systems.")}</td></tr>
                </table>
            </div>
        </section>

        <section class="section" id="projects" aria-labelledby="projects-h">
            <div class="wrap">
                <div class="section-head"><span class="num">02</span><h2 id="projects-h">{b("Projeler", "Projects")}</h2></div>
                {filt}
                <ol class="project-list">
{chr(10).join(rows)}
                </ol>
            </div>
        </section>

        <section class="section" id="contact" aria-labelledby="contact-h">
            <div class="wrap">
                <div class="section-head"><span class="num">03</span><h2 id="contact-h">{b("İletişim", "Contact")}</h2></div>
                <div class="contact-grid">
                    {B("p", "Staj, proje ya da sadece bir soru için bana e-postayla ulaşabilirsin. Projelerin kaynak kodları GitHub'da.",
                       "For internships, projects or just a question, email is the best way to reach me. Source code for the projects is on GitHub.")}
                    <table class="spec">
                        <tr><th scope="row">{b("E-posta", "Email")}</th><td><a href="mailto:mf.aksoy34@gmail.com">mf.aksoy34@gmail.com</a></td></tr>
                        <tr><th scope="row" lang="en">GitHub</th><td><a href="https://github.com/FatihAksoyEEE">FatihAksoyEEE ↗</a></td></tr>
                        <tr><th scope="row" lang="en">LinkedIn</th><td><a href="https://www.linkedin.com/in/mehmet-fatih-aksoy-1217443ba">mehmet-fatih-aksoy ↗</a></td></tr>
                        <tr><th scope="row" lang="en">YouTube</th><td><a href="https://www.youtube.com/@electronc_workshop">@electronc_workshop ↗</a></td></tr>
                        <tr><th scope="row" lang="en">Instagram</th><td><a href="https://www.instagram.com/fatih_aksoy6741/">@fatih_aksoy6741 ↗</a></td></tr>
                        <tr><th scope="row">CV</th><td><a href="assets/Mehmet_Fatih_Aksoy_CV_TR-EN.pdf" download="Mehmet_Fatih_Aksoy_CV.pdf" data-goatcounter-click="cv-indir">{b("PDF · Türkçe ve İngilizce", "PDF · Turkish and English")}</a></td></tr>
                    </table>
                </div>
            </div>
        </section>
    </main>
"""
    out += footer()
    return out


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
ROOT_FILES = re.compile(r"^(assets/|styles\.css|script\.js|favicon|apple-touch-icon)")


class Localizer(HTMLParser):
    """Bir dil için HTML'i yeniden yazar: diğer dilin data-lang elemanlarını atar,
    kök dosyalara giden göreli yolların başına `prefix` ekler."""

    def __init__(self, lang, prefix):
        super().__init__(convert_charrefs=False)
        self.lang, self.prefix, self.out, self.skip = lang, prefix, [], 0

    def fix(self, text):
        if not self.prefix:
            return text
        def rep(m):
            attr, val = m.group(1), m.group(2)
            if attr == "srcset":
                val = ", ".join(self.prefix + c if ROOT_FILES.match(c) else c for c in val.split(", "))
            elif ROOT_FILES.match(val):
                val = self.prefix + val
            return f'{attr}="{val}"'
        return re.sub(r'\b(src|href|srcset|poster)="([^"]*)"', rep, text)

    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag not in VOID:
                self.skip += 1
            return
        dl = dict(attrs).get("data-lang")
        if dl and dl != self.lang:
            if tag not in VOID:
                self.skip = 1
            return
        self.out.append(self.fix(self.get_starttag_text()))

    def handle_startendtag(self, tag, attrs):
        if not self.skip:
            self.out.append(self.fix(self.get_starttag_text()))

    def handle_endtag(self, tag):
        if self.skip:
            if tag not in VOID:
                self.skip -= 1
            return
        self.out.append(f"</{tag}>")

    def _raw(self, s):
        if not self.skip:
            self.out.append(s)

    def handle_data(self, d): self._raw(d)
    def handle_entityref(self, n): self._raw(f"&{n};")
    def handle_charref(self, n): self._raw(f"&#{n};")
    def handle_comment(self, d): self._raw(f"<!--{d}-->")
    def handle_decl(self, d): self._raw(f"<!{d}>")


def localize(s, lang, prefix=""):
    p = Localizer(lang, prefix)
    p.feed(s)
    p.close()
    return "".join(p.out)


def write(name, s):
    # Fazla boşlukları sadeleştir
    s = re.sub(r"\n\s*\n\s*\n", "\n\n", s)
    path = os.path.join(ROOT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("wrote", name, len(s))


def not_found_page():
    """GitHub Pages her eksik adreste bunu gösterir (/en/... dahil), bu yüzden yollar mutlaktır."""
    out = head("Sayfa bulunamadı · Fatih Aksoy", "Aradığın sayfa bulunamadı. Page not found.", "404.html", "tr", noindex=True)
    out += f"""<body>
    <header class="site-header">
        <div class="wrap">
            <a class="brand" href="/">Fatih Aksoy <span class="label">EEE</span></a>
        </div>
    </header>
    <main id="main" class="not-found">
        <div class="wrap">
            <p class="label">Hata 404 · <span lang="en">Error 404</span></p>
            <h1>Sinyal yok.</h1>
            <p class="lead">Bu adreste bir sayfa bulunamadı. Bağlantı eski olabilir ya da sayfa taşınmış olabilir.</p>
            <p class="lead" lang="en">There is no page at this address. The link may be outdated or the page may have moved.</p>
            <div class="actions">
                <a class="btn btn-primary" href="/">Ana sayfa <span class="arrow">→</span></a>
                <a class="btn" href="/en/" lang="en">English home <span class="arrow">→</span></a>
                <a class="btn" href="/#projects">Projeler <span class="arrow">→</span></a>
            </div>
        </div>
    </main>
""" + footer()
    return localize(out, "tr", "/")


pages = [("index.html", index_page)] + [(p["slug"], (lambda i, p: lambda lang: project_page(i, p, lang))(i, p))
                                        for i, p in enumerate(PROJECTS)]
for name, fn in pages:
    write(name, localize(fn("tr"), "tr"))
    write("en/" + name, localize(fn("en"), "en", "../"))
write("404.html", not_found_page())

LASTMOD = "2026-10-17"
urls = [""] + [p["slug"] for p in PROJECTS]
sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
      'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
for u in urls:
    alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{page_url(u, l)}"/>' for l in ("tr", "en"))
    for l in ("tr", "en"):
        sm += f"  <url><loc>{page_url(u, l)}</loc><lastmod>{LASTMOD}</lastmod>{alts}</url>\n"
sm += "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
