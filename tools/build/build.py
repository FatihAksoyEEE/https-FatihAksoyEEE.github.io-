"""Sitenin HTML sayfalarını üretir: python3 tools/build/build.py

index.html, project-*.html, sitemap.xml ve robots.txt bu betikle üretilir. Header/footer gibi
ortak parçalar common.py, proje içerikleri projects.py içindedir. Gereksinim: Pillow (görsel boyutları için).
"""
import os, re, sys, html
from PIL import Image
from common import b, B, head, header, footer, SITE
from projects import PROJECTS

# Varsayılan: repo kökü (tools/build/../..)
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
IMG = "assets/img/"


def size(path):
    with Image.open(os.path.join(ROOT, path)) as im:
        return im.size


def img(path, alt, cls="", lazy=True, extra=""):
    w, h = size(IMG + path)
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="{IMG}{path}" width="{w}" height="{h}" alt="{html.escape(alt)}"{c}{l}{extra}>'


def expand_figs(s, counter):
    def rep(m):
        path, t_tr, t_en, c_tr, c_en, cls = m.group(1).split("|")
        counter[0] += 1
        n = counter[0]
        alt = t_tr + (f": {c_tr}" if c_tr else "")
        cap = b(f"Şekil {n}", f"Fig. {n}")
        text = b(t_tr + (f" — {c_tr}" if c_tr else ""), t_en + (f" — {c_en}" if c_en else ""))
        return (f'<figure class="fig"><a href="{IMG}{path}">{img(path, alt, cls)}</a>'
                f'<figcaption><span class="label">{cap}</span>{text}</figcaption></figure>')
    return re.sub(r"\{fig:([^}]*)\}", rep, s)


def label(l):
    return b(*l) if isinstance(l, tuple) else l


# ---------------------------------------------------------------------------
def project_page(i, p):
    num = f"{i + 1:02d}"
    t_tr, t_en = p["title"]
    out = head(f"{t_tr} · Fatih Aksoy", f"{t_en} · Fatih Aksoy", p["desc"][0], p["slug"],
               og_image=(IMG + p["thumb"][0]) if p.get("thumb") else "assets/og.jpg", og_type="article")
    out += header(on_home=False, active="projects")
    meta = "\n".join(f'<div><dt class="label">{label(k)}</dt><dd>{v}</dd></div>' for k, v in p["meta"])
    counter = [0]
    toc, secs = [], []
    for j, (sid, (h_tr, h_en), body) in enumerate(p["sections"]):
        n = f"{j + 1}"
        toc.append(f'<li><a href="#{sid}"><span class="n">{n}</span>{b(h_tr, h_en)}</a></li>')
        secs.append(f'<section class="ds-section" id="{sid}" aria-labelledby="{sid}-h">\n'
                    f'<h2 id="{sid}-h"><span class="num">{num}.{n}</span>{b(h_tr, h_en)}</h2>\n'
                    f'{expand_figs(body, counter)}\n</section>')
    prev_p = PROJECTS[i - 1] if i > 0 else None
    next_p = PROJECTS[i + 1] if i + 1 < len(PROJECTS) else None
    pager = '<nav class="pager wrap" aria-label="' + "Proje gezinme" + '">'
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
                <nav class="ds-toc" aria-label="İçindekiler">
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
def index_page():
    out = head("Fatih Aksoy · Elektrik-Elektronik Mühendisliği",
               "Fatih Aksoy · Electrical & Electronics Engineering",
               "Fatih Aksoy: gömülü sistemler, PCB tasarımı ve otomasyon üzerine çalışan elektrik-elektronik mühendisliği öğrencisi. Projeler, şemalar ve kaynak kodlar.",
               "")
    out += header(on_home=True)
    rows = []
    for i, p in enumerate(PROJECTS):
        if p.get("thumb"):
            thumb = img(p["thumb"][0], "", "thumb").replace('alt=""', 'alt="" aria-hidden="true"')
        else:
            thumb = f'<span class="thumb thumb-text" aria-hidden="true">{html.escape(p["thumb_text"])}</span>'
        rows.append(f"""<li><a class="project-row" href="{p['slug']}">
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
                    <p class="label">{b("Elektrik-elektronik mühendisliği öğrencisi", "Electrical &amp; electronics engineering student")}</p>
                    <h1>Fatih Aksoy</h1>
                    {B("p", "Gömülü sistemler, PCB tasarımı ve otomasyon üzerine çalışıyorum. Kartı tasarlamaktan firmware'ini ve onu kullanan masaüstü arayüzü yazmaya kadar projenin tamamını üstlenmeyi seviyorum.",
                       "I work on embedded systems, PCB design and automation. I like owning a project end to end: from designing the board to writing its firmware and the desktop app that drives it.", 'class="lead"')}
                    <div class="actions">
                        <a class="btn btn-primary" href="#projects">{b("Projeler", "Projects")} <span class="arrow">↓</span></a>
                        <a class="btn" href="assets/FatihAksoy_CV.pdf" download="Fatih_Aksoy_CV.pdf">{b("CV indir", "Download CV")} <span class="arrow">PDF</span></a>
                        <a class="btn" href="https://github.com/FatihAksoyEEE">GitHub <span class="arrow">↗</span></a>
                    </div>
                </div>
                <figure class="hero-figure">
                    {portrait}
                    <figcaption class="label">{b("Portre · karakalem, çizgili defter", "Portrait · pencil on lined paper")}</figcaption>
                </figure>
            </div>
        </section>

        <section class="section" id="about" aria-labelledby="about-h">
            <div class="wrap">
                <div class="section-head"><span class="num">01</span><h2 id="about-h">{b("Hakkında", "About")}</h2></div>
                <div class="about-grid">
                    <div>
                        {B("p", "Merhaba, ben Fatih. Elektrik-elektronik mühendisliği öğrencisiyim. Kendimi en çok <strong>gömülü sistemler</strong>, <strong>PCB tasarımı</strong> ve <strong>otomasyon</strong> alanlarında, gerçek donanım üzerinde çalışarak geliştiriyorum.",
                           "Hi, I'm Fatih, an electrical and electronics engineering student. I learn best by working on real hardware, mostly in <strong>embedded systems</strong>, <strong>PCB design</strong> and <strong>automation</strong>.")}
                        {B("p", "Son projelerimde bir quadcopter'ın uçuş kartını KiCad'de çizdim, STM32 ile bir robot kolu sürdüm, bir aracın CAN hattını dinleyerek motor devri sinyalini tersine mühendislikle çözdüm ve bunlarla konuşan masaüstü arayüzleri yazdım.",
                           "Recently I drew a quadcopter flight board in KiCad, drove a robot arm with an STM32, reverse-engineered a vehicle's engine-speed signal by listening to its CAN bus, and wrote the desktop apps that talk to them.")}
                        <!-- TODO(Fatih): okul, sınıf ve kısa zaman çizelgesi eklenecek. -->
                    </div>
                    <table class="spec">
                        <tr><th scope="row">{b("Odak", "Focus")}</th><td>{b("Gömülü yazılım, PCB tasarımı, haberleşme protokolleri, otomasyon", "Embedded software, PCB design, communication protocols, automation")}</td></tr>
                        <tr><th scope="row">MCU</th><td>STM32, ESP32, AVR (ATmega328P)</td></tr>
                        <tr><th scope="row">{b("Donanım", "Hardware")}</th><td>KiCad, {b("şema ve PCB yerleşimi", "schematic and PCB layout")}</td></tr>
                        <tr><th scope="row">{b("Yazılım", "Software")}</th><td>C/C++ (PlatformIO, Arduino), Python (PyQt6, python-can), JavaScript (React, Electron, Node.js)</td></tr>
                        <tr><th scope="row">{b("Protokoller", "Protocols")}</th><td>CAN, UART, I²C, SPI, USB-CDC, ESP-NOW</td></tr>
                    </table>
                </div>
            </div>
        </section>

        <section class="section" id="projects" aria-labelledby="projects-h">
            <div class="wrap">
                <div class="section-head"><span class="num">02</span><h2 id="projects-h">{b("Projeler", "Projects")}</h2></div>
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
                        <!-- TODO(Fatih): LinkedIn profil linki eklenecek. -->
                        <tr><th scope="row" lang="en">YouTube</th><td><a href="https://www.youtube.com/@electronc_workshop">@electronc_workshop ↗</a></td></tr>
                        <tr><th scope="row" lang="en">Instagram</th><td><a href="https://www.instagram.com/fatih_aksoy6741/">@fatih_aksoy6741 ↗</a></td></tr>
                        <tr><th scope="row">CV</th><td><a href="assets/FatihAksoy_CV.pdf" download="Fatih_Aksoy_CV.pdf">FatihAksoy_CV.pdf</a></td></tr>
                    </table>
                </div>
            </div>
        </section>
    </main>
"""
    out += footer()
    return out


def write(name, s):
    # Fazla boşlukları sadeleştir
    s = re.sub(r"\n\s*\n\s*\n", "\n\n", s)
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(s)
    print("wrote", name, len(s))


write("index.html", index_page())
for i, p in enumerate(PROJECTS):
    write(p["slug"], project_page(i, p))

urls = [""] + [p["slug"] for p in PROJECTS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-10-16</lastmod></url>\n" for u in urls)
sm += "</urlset>\n"
write("sitemap.xml", sm)
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
