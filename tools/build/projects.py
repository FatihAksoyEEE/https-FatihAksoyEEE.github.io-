"""Proje içerikleri. Kaynaklar: ilgili GitHub repoları (README, docs, kaynak kod, KiCad çıktıları)
ve sitenin önceki sürümündeki metinler. Repolarda olmayan ölçüm/sonuç değerleri uydurulmadı."""
from common import b, B, Diagram

GH = "https://github.com/FatihAksoyEEE/"


def spec(rows, caption=None):
    cap = f'<caption class="label">{caption}</caption>' if caption else ""
    body = "\n".join(f"<tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in rows)
    return f'<table class="spec">{cap}\n{body}\n</table>'


def table(head, rows):
    th = "".join(f'<th scope="col">{h}</th>' for h in head)
    body = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-scroll"><table class="spec cols"><thead><tr>{th}</tr></thead>\n<tbody>{body}</tbody></table></div>'


def status(items):
    lis = "\n".join(f'<li class="{"done" if d else ""}">{t}</li>' for d, t in items)
    return f'<ul class="status-list">{lis}</ul>'


def links(items):
    lis = "\n".join(f'<li><span class="label" lang="en">{k}</span><a href="{u}">{t} ↗</a></li>' for k, t, u in items)
    return f'<ul class="links-list">{lis}</ul>'


# ---------------------------------------------------------------------------
# 1) CAN-Bus Sniffer
# ---------------------------------------------------------------------------
d = Diagram(760, 240, "CAN dinleme zinciri blok diyagramı")
d.box(10, 30, 140, 56, "Araç ECU'ları", "kontrol üniteleri")
d.box(10, 160, 140, 56, "OBD-II soketi", "pin 6 / 14 / 5")
d.wire([(80, 86), (80, 160)]).text(90, 128, "CAN · 500 kbit/s")
d.box(210, 160, 160, 56, "CANable V2.1", "SLCAN · listen-only", accent=True)
d.wire([(150, 188), (210, 188)], "CAN", 180, 180)
d.box(430, 160, 160, 56, "canable_logger.py", "çerçeve → CSV")
d.wire([(370, 188), (430, 188)], "USB", 400, 180)
d.box(430, 30, 160, 56, "rpm_analyzer.py", "kalibrasyon")
d.wire([(510, 160), (510, 86)]).text(520, 128, "CSV")
d.box(640, 30, 110, 56, "rpm_gauge.py", "devir saati")
d.wire([(590, 58), (640, 58)], "0x2C4", 615, 50)
d.box(640, 160, 110, 56, "rpm_live.py", "terminal RPM")
d.wire([(590, 188), (640, 188)])
CAN_DIAGRAM = d.render()

f = Diagram(760, 150, "0x2C4 çerçevesinin bayt yerleşimi")
f.text(10, 22, "CAN ID 0x2C4 · DLC 8 · örnek çerçeve", "s")
for i, byte in enumerate(["03", "C0", "00", "00", "00", "00", "00", "00"]):
    f.box(10 + i * 92, 36, 84, 46, byte, f"D{i}", accent=i < 2)
f.raw('<polyline class="wire" points="10,96 10,104 186,104 186,96"/>')
f.text(10, 126, "raw = (D0 << 8) | D1 = 0x03C0 = 960", "t")
f.text(10, 144, "RPM = raw × 0.8 = 768", "s")
f.text(746, 126, "D2–D7: bu çalışmada kullanılmadı", "s", "end")
CAN_FRAME = f.render()

CANBUS = dict(
    slug="project-canbus-sniffer.html",
    cats=["sw"],
    title=("CAN-Bus Sniffer ve RPM Çözümleme", "CAN-Bus Sniffer and RPM Decoding"),
    short=("CAN-Bus Sniffer", "CAN-Bus Sniffer"),
    year="2026",
    tags="Python · python-can · CANable · Tersine mühendislik",
    tags_en="Python · python-can · CANable · Reverse engineering",
    thumb=("canbus/canable.webp", "CANable V2.1 USB-CAN adaptörü"),
    desc=("Bir aracın OBD-II soketinden CAN trafiğini dinleyip, üreticiye özel motor devri sinyalini tersine mühendislikle bulan araç seti.",
          "A toolset that listens to a vehicle's CAN traffic through the OBD-II port and reverse-engineers the manufacturer-specific engine RPM signal."),
    meta=[(("Rol", "Role"), b("Tek geliştirici", "Sole developer")),
          (("Donanım", "Hardware"), "CANable V2.1"),
          (("Yazılım", "Software"), "Python, python-can"),
          (("Kaynak", "Source"), f'<a href="{GH}Canbus-Sniffer-CANABLEV2.1-">GitHub ↗</a>')],
    sections=[
        ("summary", ("Özet", "Summary"), "\n".join([
            B("p", "Araçların içindeki kontrol üniteleri birbirleriyle CAN hattı üzerinden konuşur. Standart OBD-II sorguları bazı değerleri verir, ama üreticiler asıl verilerin çoğunu kendi tanımladıkları mesajlarla yayınlar ve bu mesajların anlamı belgelenmemiştir.",
              "Inside a vehicle, control units talk to each other over a CAN bus. Standard OBD-II queries return some values, but manufacturers broadcast most of the real data in their own messages, and the meaning of those messages is undocumented."),
            B("p", "Bu projede bir Toyota Hilux'un OBD-II soketine <strong>sadece dinleme</strong> modunda bağlandım, ham çerçeveleri kaydettim ve farklı motor devirlerinde alınan kayıtları karşılaştırarak devir sinyalini buldum: CAN ID <code>0x2C4</code>, ilk iki bayt big-endian, ölçek <code>×0.8</code>. Ardından bu sinyali canlı gösteren bir devir saati uygulaması yazdım.",
              "In this project I connected to the OBD-II port of a Toyota Hilux in <strong>listen-only</strong> mode, logged raw frames and compared recordings taken at different engine speeds to find the RPM signal: CAN ID <code>0x2C4</code>, first two bytes big-endian, scale <code>×0.8</code>. I then wrote a tachometer app that shows this signal live."),
        ])),
        ("diagram", ("Blok diyagram", "Block diagram"), CAN_DIAGRAM),
        ("specs", ("Özellikler", "Specifications"), spec([
            (b("Adaptör", "Adapter"), "CANable V2.1 (stok SLCAN firmware)"),
            (b("Çalışma modu", "Mode"), b("<code>M1</code> silent / listen-only: hatta çerçeve gönderilmez", "<code>M1</code> silent / listen-only: no frames are transmitted")),
            (b("Bit hızı", "Bitrate"), "500 kbit/s " + b("(250 kbit/s seçilebilir)", "(250 kbit/s selectable)")),
            (b("Bağlantı", "Wiring"), "CANH → OBD pin 6 · CANL → pin 14 · GND → pin 4/5"),
            (b("Sonlandırma", "Termination"), b("Kapalı: araç hattı zaten sonlandırılmış", "Off: the vehicle bus is already terminated")),
            (b("Kayıt formatı", "Log format"), "CSV (session_id, timestamp, can_id, data_hex, raw_line)"),
            (b("Bulunan sinyal", "Decoded signal"), "<code>0x2C4</code> · D0–D1 big-endian · RPM = raw × 0.8"),
        ])),
        ("method", ("Yöntem", "Method"), "\n".join([
            B("p", "Devir sinyalini bulmak için araç sabit, vites boşta ve el freni çekiliyken üç kısa kayıt aldım: rölanti, 1500 ve 2500 d/dk. Her kayıtta gösterge veya diagnostik cihazdan okunan gerçek devir referans alındı.",
              "To find the RPM signal I took three short recordings with the vehicle stationary, in neutral, handbrake on: idle, 1500 and 2500 rpm. The actual engine speed read from the cluster or a diagnostic tool was used as reference for each."),
            '<pre><code>python3 canable_logger.py --duration 15 --output data/rpm_idle.csv\npython3 canable_logger.py --duration 15 --output data/rpm_1500.csv\npython3 canable_logger.py --duration 15 --output data/rpm_2500.csv\n\npython3 rpm_analyzer.py calibrate \\\n  --sample data/rpm_idle.csv=750 \\\n  --sample data/rpm_1500.csv=1500 \\\n  --sample data/rpm_2500.csv=2500</code></pre>',
            B("p", "<code>rpm_analyzer.py</code> her CAN ID için olası 16 bitlik alanları (başlangıç baytı, endian) tarar ve referans devirlerle en tutarlı doğrusal ilişkiyi (ölçek, ofset) veren adayı sıralar. Kayıtta standart OBD cevabı <code>41 0C A B</code> varsa doğrudan <code>((A × 256) + B) / 4</code> formülü kullanılır.",
              "<code>rpm_analyzer.py</code> scans candidate 16-bit fields (start byte, endianness) for every CAN ID and ranks the candidate that gives the most consistent linear fit (scale, offset) against the reference speeds. If the log contains a standard OBD reply <code>41 0C A B</code>, the formula <code>((A × 256) + B) / 4</code> is used directly."),
            CAN_FRAME,
        ])),
        ("software", ("Yazılım", "Software"), "\n".join([
            spec([
                ("<code>canable_logger.py</code>", b("Ham çerçeveleri canlı gösterir ve CSV'ye ekler. Her çalıştırma yeni bir oturum kimliği üretir.", "Shows raw frames live and appends them to CSV. Each run creates a new session id.")),
                ("<code>rpm_analyzer.py</code>", b("Kayıtları tarar, RPM adaylarını sıralar ve kalibre eder.", "Scans logs, ranks RPM candidates and calibrates them.")),
                ("<code>rpm_live.py</code>", b("Terminalde yalnızca devir değerini gösterir.", "Prints only the engine speed in the terminal.")),
                ("<code>rpm_gauge.py</code>", b("Analog/dijital devir saati. Ölçek canlı ayarlanabilir, kayıtlı CSV oynatılabilir.", "Analog/digital tachometer. Scale is adjustable live; recorded CSVs can be replayed.")),
                ("CANalyzer", b("SavvyCAN benzeri genel analiz uygulaması: live/trace görünümü, DBC ile decode, filtre, grafik, periyodik gönderim, CSV/ASC/JSON log.", "A SavvyCAN-like general analyzer: live/trace views, DBC decoding, filters, plots, periodic transmit, CSV/ASC/JSON logs.")),
            ]),
            B("p", "Örnek terminal çıktısı:", "Sample terminal output:"),
            '<pre><code>     1.242s  RPM:   768.0  raw: 03 C0 00 00 00 00 00 00</code></pre>',
            B("p", "CANalyzer'ın Dashboard sekmesinde devir saati, gaz pedalı sinyali ve tezgâh testi için sanal gaz pedalı bir arada:",
              "CANalyzer's Dashboard tab combines the tachometer, the throttle pedal signal and a virtual throttle pedal for bench testing:"),
            "{fig:canbus/canalyzer-dashboard.webp|CANalyzer Dashboard|CANalyzer Dashboard|Gösterge (0x2C4, ×0.8) ve gaz pedalı (0x2C1) yapılandırması, sanal pedal ve ACİL STOP.|Gauge (0x2C4, ×0.8) and throttle pedal (0x2C1) configuration, virtual pedal and EMERGENCY STOP.|}",
            "{fig:canbus/canalyzer-filter.webp|Filtre paneli|Filter panel|Yön (RX/TX), ID aralığı ve ID listesine göre filtreleme.|Filtering by direction (RX/TX), ID range and an ID list.|}",
            "{vid:canbus/demo-bench.mp4|canbus/demo-bench-poster.webp|Tezgâh testi|Bench test|CANable'a bağlanıp sanal gaz pedalıyla <code>0x2C1</code> çerçevelerinin her 32 ms'de gönderilmesi.|Connecting to the CANable and sending <code>0x2C1</code> frames every 32 ms with the virtual throttle pedal.}",
            "{vid:canbus/demo-tour.mp4|canbus/demo-tour-poster.webp|Arayüz turu|Interface tour|Bağlantı, gönderim (OBD-II hazır sorguları dahil) ve filtre sekmeleri.|Connection, send (including OBD-II presets) and filter tabs.}",
        ])),
        ("learned", ("Sonuçlar ve öğrenilenler", "Results and lessons"), "\n".join([
            '<ul>',
            B("li", "Üreticiye özel yayın sinyali (<code>0x2C4</code>) sürekli geldiği için canlı izleme için OBD sorgusundan daha uygun: hatta hiçbir istek göndermek gerekmiyor.",
              "The manufacturer broadcast (<code>0x2C4</code>) arrives continuously, so it suits live monitoring better than OBD polling: no request ever has to be sent on the bus."),
            B("li", "Araca bağlanırken güvenlik öncelikli: adaptör listen-only modda açılıyor, 5V çıkışı ve sonlandırma direnci kullanılmıyor.",
              "Safety first when connecting to a vehicle: the adapter opens in listen-only mode, and neither its 5V output nor its termination resistor is used."),
            B("li", "OBD soketinin arkasında bir gateway varsa araç içi bazı ağlar görünmeyebilir. Bu yüzden önce hangi mesajların göründüğünü kaydetmek gerekiyor.",
              "If there is a gateway behind the OBD port, some in-vehicle networks may not be visible, so the first step is always to log what is actually there."),
            '</ul>',
        ])),
        ("links", ("Bağlantılar", "Links"), links([
            ("GitHub", "FatihAksoyEEE/Canbus-Sniffer-CANABLEV2.1-", GH + "Canbus-Sniffer-CANABLEV2.1-"),
        ])),
    ],
)

# ---------------------------------------------------------------------------
# 2) Yer Kontrol İstasyonu
# ---------------------------------------------------------------------------
d = Diagram(760, 230, "Yer kontrol istasyonu blok diyagramı")
d.box(10, 85, 130, 56, "İHA", "uçuş kontrolcüsü")
d.box(190, 85, 140, 56, "Telsiz / seri", "57600 baud")
d.wire([(140, 113), (190, 113)], arrow=True, both=True)
d.box(380, 85, 150, 56, "Electron main", "serialport · IPC", accent=True)
d.wire([(330, 113), (380, 113)], arrow=True, both=True)
d.box(590, 15, 160, 50, "Paket ayrıştırıcı", "DataView · 0xAA 0xBB")
d.box(590, 90, 160, 50, "PFD + telemetri", "ufuk · şeritler")
d.box(590, 165, 160, 50, "Görev planlayıcı", "Leaflet · waypoint")
d.wire([(530, 100), (560, 100), (560, 40), (590, 40)]).text(552, 62, "telemetri", "s", "end")
d.wire([(670, 65), (670, 90)])
d.wire([(590, 190), (560, 190), (560, 126), (530, 126)]).text(552, 170, "görev", "s", "end")
GCS_DIAGRAM = d.render()

GCS = dict(
    slug="project-control-station.html",
    cats=["sw"],
    title=("Yer Kontrol İstasyonu: LoRa Kontrolcü ve Alıcı Tasarımı", "Ground Control Station: LoRa Controller and Receiver Design"),
    short=("Yer Kontrol İstasyonu: LoRa Kontrolcü ve Alıcı", "Ground Control Station: LoRa Controller and Receiver"),
    year="2026",
    tags="LoRa · React · Electron · Seri haberleşme",
    tags_en="LoRa · React · Electron · Serial comms",
    thumb=("control-station/controller-thumb.webp", "LoRa kumanda"),
    desc=("İHA'lar için masaüstü yer kontrol yazılımı: seri hattan gelen telemetriyi çözer, uçuş göstergelerini çizer ve harita üzerinden görev yükler.",
          "Desktop ground control software for UAVs: decodes telemetry from a serial link, draws flight instruments and uploads missions from a map."),
    meta=[(("Rol", "Role"), b("Tek geliştirici", "Sole developer")),
          (("Platform", "Platform"), "Electron (macOS / Windows)"),
          (("Yığın", "Stack"), "React 19, Vite, Leaflet"),
          (("Kaynak", "Source"), f'<a href="{GH}Ground-Control-System">GitHub ↗</a>')],
    sections=[
        ("summary", ("Özet", "Summary"), "\n".join([
            B("p", "Uçuş sırasında operatörün aracın durumunu tek ekranda görmesi ve rotayı uçuş sırasında değiştirebilmesi gerekiyor. Hazır yer istasyonları (Mission Planner, QGroundControl) MAVLink'e bağlı; benim kartlarım ise kendi tanımladığım daha küçük bir ikili protokol kullanıyor.",
              "During a flight the operator needs to see the vehicle's state on one screen and be able to change the route on the fly. Off-the-shelf ground stations (Mission Planner, QGroundControl) are tied to MAVLink, whereas my boards use a smaller binary protocol I defined myself."),
            B("p", "Bu yüzden Electron üzerinde çalışan bir yer kontrol istasyonu yazdım. Seri porttan gelen paketleri çözüyor, yapay ufuk ve hız/irtifa şeritleriyle bir birincil uçuş ekranı (PFD) çiziyor ve harita üzerinde oluşturulan görevi sağlama toplamıyla birlikte araca gönderiyor.",
              "So I wrote a ground control station that runs on Electron. It decodes packets from the serial port, draws a primary flight display (PFD) with an artificial horizon and speed/altitude tapes, and sends a mission built on the map to the vehicle with a checksum."),
        ])),
        ("diagram", ("Blok diyagram", "Block diagram"), GCS_DIAGRAM),
        ("protocol", ("Telemetri paketi", "Telemetry packet"), "\n".join([
            B("p", "Araçtan gelen her paket 34 bayt. <code>0xAA 0xBB</code> başlığıyla senkronize olunuyor, alanlar little-endian ve ölçekli tam sayı olarak taşınıyor.",
              "Every packet from the vehicle is 34 bytes. The parser syncs on the <code>0xAA 0xBB</code> header; fields are little-endian scaled integers."),
            table([b("Ofset", "Offset"), b("Tip", "Type"), b("Alan", "Field"), b("Ölçek", "Scale")], [
                ["0–1", "u8 ×2", "header", "<code>0xAA 0xBB</code>"],
                ["2", "int16", "roll", "/100 → °"],
                ["4", "int16", "pitch", "/100 → °"],
                ["6", "int16", "yaw", "/100 → °"],
                ["8", "int16", b("irtifa", "altitude"), "/10 → m"],
                ["10", "int16", b("hız", "speed"), "/100 → m/s"],
                ["12", "uint8", b("batarya", "battery"), "/10 → V"],
                ["13", "uint8", b("uydu sayısı", "satellites"), "—"],
                ["14", "uint8", "GPS fix", "—"],
                ["15", "uint8", b("uçuş modu", "flight mode"), "—"],
                ["16", "int32", b("enlem", "latitude"), "/10⁷ → °"],
                ["20", "int32", b("boylam", "longitude"), "/10⁷ → °"],
            ]),
            B("p", "Görev yüklenirken her waypoint 11 bayta paketleniyor: enlem ve boylam <code>float32</code>, irtifa <code>int16</code>, komut <code>uint8</code> (16 waypoint, 20 RTL, 21 land, 22 takeoff). Paket sonunda iki baytlık Fletcher-16 sağlama toplamı var.",
              "When a mission is uploaded, each waypoint is packed into 11 bytes: latitude and longitude as <code>float32</code>, altitude as <code>int16</code>, command as <code>uint8</code> (16 waypoint, 20 RTL, 21 land, 22 takeoff). The packet ends with a two-byte Fletcher-16 checksum."),
        ])),
        ("features", ("Özellikler", "Features"), spec([
            ("PFD", b("Yapay ufuk, hız ve irtifa şeritleri, dairesel göstergeler", "Artificial horizon, speed and altitude tapes, circular gauges")),
            (b("Harita", "Map"), b("Leaflet ile canlı konum, rota çizimi, sürükle-bırak waypoint düzenleme", "Live position with Leaflet, route drawing, drag-and-drop waypoint editing")),
            (b("Güvenlik", "Safety"), b("Waypoint'lerin zemin yüksekliği sorgulanır; minimum güvenli irtifanın altındakiler uyarı verir", "Ground elevation is fetched for each waypoint; those below the minimum safe altitude raise a warning")),
            (b("Performans", "Performance"), b("Arayüz yenileme hızı sınırlanır (throttle), gelen veri tamponda biriktirilir", "UI refresh rate is throttled; incoming data is buffered")),
            (b("Kalıcılık", "Persistence"), b("Tema, birimler, baud hızı ve sesli uyarı ayarları saklanır; görev JSON olarak kaydedilip yüklenebilir", "Theme, units, baud rate and audio alert settings persist; missions save/load as JSON")),
            ("Setup", b("Gövde tipi seçimi, motor testi ve yön, servo min/max/trim sınırları (arayüz)", "Frame type selection, motor test and direction, servo min/max/trim limits (UI)")),
        ])),
        ("status", ("Durum", "Status"), status([
            (True, b("Seri port yönetimi ve ikili protokol ayrıştırıcı", "Serial port management and binary protocol parser")),
            (True, b("PFD, harita ve telemetri panelleri", "PFD, map and telemetry panels")),
            (True, b("Waypoint yükleme ve uçuş sırasında rota değiştirme", "Waypoint upload and in-flight re-routing")),
            (False, b("Araçtaki görevi geri okuma (waypoint download)", "Reading the mission back from the vehicle (waypoint download)")),
            (False, b("USB gamepad ile RC override", "RC override with a USB gamepad")),
            (False, b("Setup ekranındaki ayarların araca yazılması", "Writing Setup screen settings to the vehicle")),
        ])),
        ("links", ("Bağlantılar", "Links"), links([
            ("GitHub", "FatihAksoyEEE/Ground-Control-System", GH + "Ground-Control-System"),
        ])),
    ],
)

# ---------------------------------------------------------------------------
# 3) Robot kol
# ---------------------------------------------------------------------------
d = Diagram(760, 210, "Robot kol kontrol sistemi blok diyagramı")
d.box(10, 75, 150, 56, "PyQt6 arayüz", "slider · HOME")
d.box(220, 75, 160, 56, "STM32F411CE", "Blackpill · USB-CDC", accent=True)
d.wire([(160, 103), (220, 103)], "USB", 190, 95, both=True)
d.box(460, 15, 130, 46, "TIM1 CH1–3", "PA8 · PA9 · PA10")
d.box(460, 145, 130, 46, "TIM4 CH1–3", "PB6 · PB7 · PB8")
d.wire([(380, 95), (420, 95), (420, 38), (460, 38)], "PWM 50 Hz", 420, 30)
d.wire([(380, 111), (420, 111), (420, 168), (460, 168)])
d.box(640, 15, 110, 46, "Servo 1–3")
d.box(640, 145, 110, 46, "Servo 4–6")
d.wire([(590, 38), (640, 38)])
d.wire([(590, 168), (640, 168)])
d.box(640, 80, 110, 46, "5 V / 10 A", "servo gücü")
d.wire([(695, 80), (695, 61)])
d.wire([(695, 126), (695, 145)])
ARM_DIAGRAM = d.render()

ARM = dict(
    slug="project-robot-arm.html",
    cats=["fw", "sw"],
    title=("6 Eksenli Robot Kol Kontrolcüsü", "6-Axis Robot Arm Controller"),
    short=("Robot Kol Kontrolcüsü", "Robot Arm Controller"),
    year="2026",
    tags="STM32 · PlatformIO · PyQt6",
    tags_en="STM32 · PlatformIO · PyQt6",
    thumb=("robot-arm/cover.webp", "Robot kolun 3D modeli"),
    desc=("STM32 Blackpill üzerinde çalışan 6 servolu robot kol firmware'i ve USB üzerinden kontrol eden PyQt6 masaüstü arayüzü.",
          "Firmware for a 6-servo robot arm on an STM32 Blackpill, plus a PyQt6 desktop app that controls it over USB."),
    meta=[(("Rol", "Role"), b("Tek geliştirici", "Sole developer")),
          ("MCU", "STM32F411CE"),
          (("Yazılım", "Software"), "C++ (STM32duino), Python"),
          (("Kaynak", "Source"), f'<a href="{GH}RoboArm">GitHub ↗</a>')],
    sections=[
        ("summary", ("Özet", "Summary"), "\n".join([
            B("p", "Altı servolu bir robot kolu bilgisayardan kontrol etmek için bir firmware ve bir masaüstü arayüzü yazdım. STM32, bilgisayara USB-CDC ile sanal seri port olarak bağlanıyor; ayrı bir USB-UART dönüştürücüye gerek kalmıyor.",
              "I wrote firmware and a desktop app to control a six-servo robot arm from a computer. The STM32 shows up as a virtual serial port over USB-CDC, so no separate USB-UART converter is needed."),
            B("p", "Komut seti bilinçli olarak düz metin tutuldu: aynı komutlar arayüzden de, <code>screen</code> gibi bir seri terminalden de gönderilebiliyor. Bu, donanımı arayüzden bağımsız olarak test etmeyi kolaylaştırıyor.",
              "The command set is deliberately plain text: the same commands can be sent from the GUI or from a serial terminal such as <code>screen</code>. That makes it easy to test the hardware independently of the GUI."),
        ])),
        ("diagram", ("Blok diyagram", "Block diagram"), ARM_DIAGRAM),
        ("model", ("3D model", "3D model"), "\n".join([
            '<div class="fig-pair">',
            "{fig:robot-arm/cad-01.webp|Perspektif|Perspective|Kolun 3D modeli, eklem açılarıyla.|3D model of the arm with joint angles.|}",
            "{fig:robot-arm/cad-02.webp|Yan görünüm|Side view|Kol dik konumda.|Arm in upright pose.|}",
            '</div>',
        ])),
        ("hardware", ("Donanım", "Hardware"), "\n".join([
            spec([
                ("MCU", "STM32 Blackpill F411CE"),
                (b("Aktüatörler", "Actuators"), b("6 × PWM servo", "6 × PWM servo")),
                ("PWM", b("50 Hz (20 ms), 16 bit çözünürlük; 0° = 1000 µs, 90° = 1500 µs, 180° = 2000 µs", "50 Hz (20 ms), 16-bit resolution; 0° = 1000 µs, 90° = 1500 µs, 180° = 2000 µs")),
                (b("Zamanlayıcılar", "Timers"), "TIM1 CH1–3 (PA8, PA9, PA10) · TIM4 CH1–3 (PB6, PB7, PB8)"),
                (b("Güç", "Power"), b("Servolar için ayrı 5 V / 10 A kaynak; STM32 USB'den beslenir", "Separate 5 V / 10 A supply for the servos; the STM32 is powered from USB")),
                (b("Haberleşme", "Comms"), "USB-CDC, 115200 baud"),
            ]),
            '<pre><code>duty = (pulse_us × 65535) / 20000\n\n  0° → (1000 × 65535) / 20000 = 3277\n 90° → (1500 × 65535) / 20000 = 4915\n180° → (2000 × 65535) / 20000 = 6554</code></pre>',
            B("p", "<strong>Ortak toprak:</strong> Servo kaynağının eksi ucu STM32 GND'sine bağlanmazsa PWM sinyalinin referansı kayar ve servolar hareket etmez. Servo uçlarına konan 100 µF kapasitörler ani akım çekişlerinde gerilim çökmelerini azaltıyor.",
              "<strong>Common ground:</strong> if the servo supply's negative terminal is not tied to the STM32 GND, the PWM reference floats and the servos do not move. 100 µF capacitors at the servo connectors reduce voltage dips during current spikes."),
        ])),
        ("software", ("Yazılım", "Software"), "\n".join([
            table([b("Komut", "Command"), b("İşlev", "Function"), b("Örnek", "Example")], [
                ["<code>S&lt;n&gt;:" + b("&lt;açı&gt;", "&lt;angle&gt;") + "</code>", b("n. servoyu açıya getir (n = 1–6, açı = 0–180)", "Move servo n to angle (n = 1–6, angle = 0–180)"), "<code>S1:90</code>"],
                ["<code>ALL:" + b("&lt;açı&gt;", "&lt;angle&gt;") + "</code>", b("Tüm servoları aynı açıya getir", "Move all servos to one angle"), "<code>ALL:90</code>"],
                ["<code>STATUS</code>", b("Tüm açıları raporla", "Report all angles"), "<code>S1:90,S2:45,…</code>"],
                ["<code>RESET</code>", b("Tüm servoları 90°'ye döndür", "Return all servos to 90°"), "<code>RESET</code>"],
            ]),
            B("p", "Hatalı komutlara açık hata mesajları dönüyor (<code>ERROR:Angle out of range</code>, <code>ERROR:Servo ID out of range</code> vb.). Arayüzde her servo için bir slider ve min/max açı sınırı var; HOME, RESET ve STATUS butonları aynı komutları gönderiyor. Arayüz macOS için <code>py2app</code> ile tek bir <code>.app</code> olarak paketlenebiliyor.",
              "Bad commands get explicit error replies (<code>ERROR:Angle out of range</code>, <code>ERROR:Servo ID out of range</code>, etc.). The GUI has a slider and min/max limits per servo; HOME, RESET and STATUS buttons send the same commands. On macOS the GUI can be bundled into a single <code>.app</code> with <code>py2app</code>."),
        ])),
        ("links", ("Bağlantılar", "Links"), links([
            ("GitHub", "FatihAksoyEEE/RoboArm", GH + "RoboArm"),
        ])),
    ],
)

# ---------------------------------------------------------------------------
# 4) ESP32 Quadcopter (eski "Otonom İHA" sayfası)
# ---------------------------------------------------------------------------
d = Diagram(760, 250, "ESP32 quadcopter kartı blok diyagramı")
d.box(10, 20, 130, 50, "USB-C", "5 V")
d.box(10, 100, 130, 50, "TP4056", "1S Li-Po şarj")
d.box(10, 180, 130, 50, "Li-Po 1S", "+BATT")
d.wire([(75, 70), (75, 100)])
d.wire([(75, 150), (75, 180)], both=True)
d.box(200, 20, 150, 50, "CP2102N", "USB-UART")
d.wire([(140, 45), (200, 45)])
d.box(200, 100, 150, 50, "MIC5219-3.3", "LDO · 3V3")
d.wire([(140, 205), (170, 205), (170, 125), (200, 125)])
d.box(410, 85, 160, 80, "ESP32-WROOM-32", "Wi-Fi · ESP-NOW", accent=True)
d.wire([(350, 45), (490, 45), (490, 85)], "TX/RX", 420, 37)
d.wire([(350, 125), (410, 125)], "3V3", 380, 117)
d.box(630, 20, 120, 50, "MPU-6050", "IMU · I²C")
d.wire([(570, 105), (600, 105), (600, 45), (630, 45)]).text(606, 80, "I²C", "s")
d.box(630, 110, 120, 50, "4 × SI2302", "fırçalı motor")
d.wire([(570, 135), (630, 135)], "PWM", 600, 127)
d.box(410, 195, 160, 40, "ADC_BAT · IO35", "batarya gerilimi")
d.wire([(490, 195), (490, 165)])
QUAD_DIAGRAM = d.render()

QUAD = dict(
    slug="project-uav.html",
    cats=["pcb", "fw"],
    title=("ESP32 Quadcopter Uçuş Kartı", "ESP32 Quadcopter Flight Board"),
    short=("ESP32 Quadcopter", "ESP32 Quadcopter"),
    year="2025",
    tags="PCB · KiCad · ESP32 · Firmware",
    tags_en="PCB · KiCad · ESP32 · Firmware",
    thumb=("quadcopter/pcb-3d.webp", "ESP32 quadcopter kartının 3D görünümü"),
    desc=("Gövdesi de PCB olan, ESP32 tabanlı küçük bir quadcopter: şema, kart tasarımı ve PID stabilizasyonlu uçuş yazılımı.",
          "A small ESP32-based quadcopter whose frame is the PCB itself: schematic, board layout and PID-stabilised flight firmware."),
    meta=[(("Rol", "Role"), b("Tasarım ve yazılım", "Design and firmware")),
          ("MCU", "ESP32-WROOM-32"),
          (("Araçlar", "Tools"), "KiCad, PlatformIO"),
          (("Kaynak", "Source"), f'<a href="{GH}ESP32_Drone">GitHub ↗</a>')],
    sections=[
        ("summary", ("Özet", "Summary"), "\n".join([
            B("p", "Amaç, uçuş kontrolcüsünü hazır bir kart almadan sıfırdan tasarlamak ve bu sırada güç, sensör ve motor sürme tarafını tek kartta çözmekti. Kartın kolları aynı zamanda gövde: motorlar kolların uçlarındaki yuvalara oturuyor.",
              "The goal was to design a flight controller from scratch instead of buying one, solving power, sensing and motor drive on a single board. The board's arms are also the frame: the motors sit in the mounts at the ends of the arms."),
            B("p", "ESP32'nin iki çekirdeği iş bölümü için kullanılıyor: bir çekirdek sensör okuma ve PID döngüsünü, diğeri yer istasyonuyla haberleşmeyi yürütüyor.",
              "The ESP32's two cores split the work: one runs sensor reads and the PID loop, the other handles communication with the ground station."),
        ])),
        ("diagram", ("Blok diyagram", "Block diagram"), QUAD_DIAGRAM),
        ("hardware", ("Donanım", "Hardware"), "\n".join([
            spec([
                ("MCU", "ESP32-WROOM-32 (dual-core, 240 MHz)"),
                ("IMU", "MPU-6050 · I²C (SDA IO21, SCL IO22)"),
                (b("Motor sürme", "Motor drive"), b("4 × SI2302 N-MOSFET, low-side; her motorda 1N4148W serbest geçiş diyodu ve 1 µF kapasitör", "4 × SI2302 N-MOSFET, low-side; 1N4148W flyback diode and 1 µF capacitor on each motor")),
                (b("Motor pinleri", "Motor pins"), "MOT_1 IO4 · MOT_2 IO33 · MOT_3 IO32 · MOT_4 IO25"),
                (b("Güç", "Power"), b("1S Li-Po; TP4056 ile USB-C'den şarj; MIC5219 3.3 V LDO; AO3401 ile USB/batarya yol seçimi", "1S Li-Po; charged from USB-C via TP4056; MIC5219 3.3 V LDO; AO3401 for USB/battery path selection")),
                (b("Programlama", "Programming"), b("CP2102N USB-UART, otomatik reset/boot devresi", "CP2102N USB-UART with auto reset/boot circuit")),
                (b("Diğer", "Other"), b("Batarya gerilimi ölçümü (IO35), açma/kapama devresi, 3 debug LED'i, genişleme konnektörü (UART2, I²C)", "Battery voltage sense (IO35), on/off circuit, 3 debug LEDs, expansion header (UART2, I²C)")),
            ]),
            "{fig:quadcopter/schematic.webp|Şema|Schematic|KiCad şeması: regülatör, şarj, USB-UART, SoC, IMU ve motor sürücüleri.|KiCad schematic: regulator, charger, USB-UART, SoC, IMU and motor drivers.|on-white}",
            '<div class="fig-grid">',
            "{fig:quadcopter/pcb-front.webp|PCB, üst katman|PCB, top layer|Üst bakır katmanı öne alınmış yerleşim; kollar ve motor yuvaları kartın parçası.|Layout with the top copper layer in front; arms and motor mounts are part of the PCB.|}",
            "{fig:quadcopter/pcb-back.webp|PCB, alt katman|PCB, bottom layer|Alt bakır katmanı öne alınmış yerleşim.|Layout with the bottom copper layer in front.|}",
            "{fig:quadcopter/pcb-3d-top.webp|3D görünüm|3D view|Kartın üstten KiCad 3D görünümü.|Top-down KiCad 3D view of the board.|}",
            '</div>',
        ])),
        ("software", ("Yazılım", "Software"), "\n".join([
            '<ul>',
            B("li", "<strong>Core 0:</strong> MPU-6050 okuma, complementary filtre ile ivmeölçer ve jiroskop füzyonu, roll/pitch/yaw PID döngüsü.",
              "<strong>Core 0:</strong> MPU-6050 reads, accelerometer/gyro fusion with a complementary filter, roll/pitch/yaw PID loop."),
            B("li", "<strong>Core 1:</strong> ESP-NOW (veya Wi-Fi üzerinden UDP) ile kumanda ve telemetri.",
              "<strong>Core 1:</strong> control input and telemetry over ESP-NOW (or UDP over Wi-Fi)."),
            '</ul>',
        ])),
        ("status", ("Durum", "Status"), status([
            (True, b("Şema ve PCB tasarımı", "Schematic and PCB design")),
            (True, b("PID stabilizasyonu ve complementary filtre", "PID stabilisation and complementary filter")),
            (False, b("GPS tabanlı otonom rota takibi (geliştirme aşamasında)", "GPS-based autonomous waypoint following (in development)")),
        ])),
        ("links", ("Bağlantılar", "Links"), links([
            ("GitHub", "FatihAksoyEEE/ESP32_Drone", GH + "ESP32_Drone"),
        ])),
    ],
)

# ---------------------------------------------------------------------------
# 5) STM32 Flight Controller
# ---------------------------------------------------------------------------
FC = dict(
    slug="project-flight-controller.html",
    cats=["pcb", "fw"],
    title=("STM32 Uçuş Kontrol Kartı", "STM32 Flight Controller Board"),
    short=("STM32 Uçuş Kontrol Kartı", "STM32 Flight Controller"),
    year="2024",
    tags="PCB · STM32 · Gömülü",
    tags_en="PCB · STM32 · Embedded",
    thumb=("flight-controller/pcb-3d.webp", "STM32 uçuş kontrol kartının 3D görünümü"),
    desc=("STM32 tabanlı, özel tasarım uçuş kontrol kartı ve stabilizasyon yazılımı.",
          "A custom STM32-based flight control board and stabilisation firmware."),
    meta=[(("Rol", "Role"), b("Kart tasarımı ve yazılım", "Board design and firmware")),
          ("MCU", "STM32"),
          (b("Yazılım", "Software"), "FreeRTOS, PID"),
          (b("Durum", "Status"), b("Belgeleniyor", "Being documented"))],
    sections=[
        ("summary", ("Özet", "Summary"), "\n".join([
            B("p", "STM32 mikrodenetleyici etrafında tasarlanmış bir uçuş kontrol kartı. Kart üzerinde ESC/servo çıkışları için GND-5V-SIG pin sıraları, alıcı ve telemetri için ayrı UART'lar, harici sensörler için SPI konnektörü ve durum LED'leri bulunuyor. Yazılım tarafında FreeRTOS üzerinde PID kontrol ve IMU sensör füzyonu hedefleniyor.",
              "A flight control board designed around an STM32 microcontroller. The board carries GND-5V-SIG headers for ESC/servo outputs, separate UARTs for receiver and telemetry, an SPI header for external sensors, and status LEDs. On the firmware side it targets PID control and IMU sensor fusion on FreeRTOS."),
            B("p", "Aynı dönemde otonom bir İHA üzerinde OpenCV ile görüntü işleme ve rota takibi üzerinde de çalıştım.",
              "In the same period I also worked on image processing and route tracking with OpenCV for an autonomous UAV."),
            "{fig:flight-controller/pcb-3d.webp|3D görünüm|3D view|Kartın 3D render'ı.|3D render of the board.|}",
            "<!-- TODO(Fatih): MCU modeli, IMU, şema/PCB görselleri, test sonuçları ve repo linki eklenecek. -->",
            '<p class="note">' + b("Bu sayfanın şema, özellik tablosu ve test sonuçları bölümleri hazırlanıyor.", "Schematic, specifications and test results for this page are being prepared.") + "</p>",
        ])),
    ],
)

# ---------------------------------------------------------------------------
# 6) CNC
# ---------------------------------------------------------------------------
d = Diagram(760, 290, "CNC kontrol kartı blok diyagramı")
d.box(10, 20, 130, 50, "12–36 V giriş")
d.box(200, 20, 140, 50, "LM2596", "12 V · motorlar")
d.wire([(140, 45), (200, 45)])
d.box(200, 90, 140, 50, "LM7805", "5 V · lojik")
d.wire([(270, 70), (270, 90)])
d.wire([(340, 45), (680, 45), (680, 150)], "12 V", 510, 37)
d.box(10, 165, 130, 50, "G-code", "bilgisayar · USB")
d.box(390, 150, 150, 70, "Arduino Nano", "ATmega328P · GRBL", accent=True)
d.wire([(140, 190), (390, 190)], "USB", 265, 182)
d.wire([(340, 115), (365, 115), (365, 165), (390, 165)]).text(372, 108, "5 V", "s")
d.box(610, 150, 140, 50, "3 × step sürücü", "X · Y · Z")
d.wire([(540, 175), (610, 175)], "STEP/DIR", 575, 167)
d.box(610, 230, 140, 50, "Step motorlar", "+ 500 W DC spindle")
d.wire([(680, 200), (680, 230)])
CNC_DIAGRAM = d.render()

CNC = dict(
    slug="project-cnc.html",
    cats=["pcb"],
    title=("3 Eksenli CNC Freze", "3-Axis CNC Mill"),
    short=("3 Eksenli CNC Freze", "3-Axis CNC Mill"),
    year="2024",
    tags="Mekanik · PCB · GRBL",
    tags_en="Mechanical · PCB · GRBL",
    thumb=("cnc/cover.webp", "CNC freze makinesinin 3D modeli"),
    desc=("Mekaniği, kontrol kartı ve yazılımıyla baştan tasarlanmış masaüstü CNC freze.",
          "A desktop CNC mill designed from scratch: mechanics, control board and software."),
    meta=[(("Rol", "Role"), b("Mekanik, elektronik, yazılım", "Mechanics, electronics, software")),
          (b("İşleme alanı", "Work area"), "200 × 150 × 200 mm"),
          ("Spindle", "500 W DC"),
          ("Firmware", "GRBL")],
    sections=[
        ("summary", ("Özet", "Summary"), "\n".join([
            B("p", "Alüminyum ve PVC gibi malzemeleri işleyebilen, tamamen kendi tasarımım olan 3 eksenli bir CNC freze. X, Y ve Z eksenleri step motorlarla sürülüyor; mekanik yapı, kontrol kartı ve yazılım projenin parçası.",
              "A fully custom 3-axis CNC mill able to machine materials such as aluminium and PVC. The X, Y and Z axes are driven by stepper motors; the mechanical structure, control board and software are all part of the project."),
            "{fig:cnc/cover.webp|Genel görünüm|Overview|Makinenin 3D modeli.|3D model of the machine.|}",
        ])),
        ("diagram", ("Blok diyagram", "Block diagram"), CNC_DIAGRAM),
        ("specs", ("Özellikler", "Specifications"), spec([
            (b("Strok", "Travel"), "X 200 mm · Y 150 mm · Z 200 mm"),
            (b("Eksen sürme", "Axis drive"), b("3 × step motor, modüler step sürücüler", "3 × stepper motor, modular stepper drivers")),
            ("Spindle", "500 W DC " + b("motor", "motor")),
            (b("Kontrolcü", "Controller"), "Arduino Nano (ATmega328P)"),
            (b("Besleme", "Supply"), "12–36 V " + b("giriş", "input")),
            (b("Regülasyon", "Regulation"), "LM2596 → 12 V " + b("(motorlar)", "(motors)") + " · LM7805 → 5 V " + b("(lojik)", "(logic)")),
            ("Firmware", "GRBL"),
            (b("Malzeme", "Materials"), b("Alüminyum, PVC", "Aluminium, PVC")),
        ])),
        ("mechanical", ("Mekanik tasarım", "Mechanical design"), "\n".join([
            B("p", "Gövde alüminyum profillerden oluşuyor, eksenlerde dayanıklılık için çelik dişli miller kullanıldı.",
              "The frame is built from aluminium extrusions; steel lead screws are used on the axes for durability."),
            '<div class="fig-grid">',
            *[f"{{fig:cnc/render-0{i}.webp|Mekanik {i}|Mechanical {i}|||}}" for i in range(1, 8)],
            '</div>',
        ])),
        ("electronics", ("Elektronik tasarım", "Electronic design"), "\n".join([
            B("p", "Kontrol kartında Arduino Nano modülü kullanıldı: kolayca değiştirilebiliyor, ucuz ve programlaması kolay. Kart üç step motoru üç modüler sürücüyle sürüyor. 12–36 V aralığındaki girişten LM2596 ile motorlar için sabit ve gürültüsüz 12 V, LM7805 ile mikrodenetleyici için 5 V üretiliyor.",
              "The control board uses an Arduino Nano module: it is easy to replace, cheap and simple to program. The board drives three steppers through three modular drivers. From the 12–36 V input, an LM2596 produces a stable, low-noise 12 V for the motors and an LM7805 produces 5 V for the microcontroller."),
            B("p", "Kartta 5 durum LED'i var: yeşil 12–36 V girişini, kırmızı 5 V hattını, üç beyaz LED ise X, Y ve Z motor çıkışlarına (OUT1–OUT3) sinyal gittiğini gösteriyor.",
              "The board has 5 status LEDs: green for the 12–36 V input, red for the 5 V rail, and three white LEDs showing signal activity on the X, Y and Z motor outputs (OUT1–OUT3)."),
            "{fig:cnc/schematic.webp|Şema|Schematic|Kontrol kartı şeması.|Control board schematic.|on-white}",
            "{fig:cnc/pcb.webp|PCB|PCB|Kontrol kartı PCB tasarımı.|Control board PCB design.|on-white}",
        ])),
        ("software", ("Yazılım", "Software"), "\n".join([
            B("p", "Makine GRBL firmware'i ile çalışıyor; G-code yorumlama ve hareket planlama GRBL tarafından yapılıyor. Geliştirme Arduino IDE ile yapıldı.",
              "The machine runs GRBL firmware, which handles G-code interpretation and motion planning. Development was done in the Arduino IDE."),
        ])),
    ],
)

# ---------------------------------------------------------------------------
# 7) DigiTab
# ---------------------------------------------------------------------------
d = Diagram(760, 190, "DigiTab mimari diyagramı")
d.box(10, 20, 150, 50, "Garson", "mobil · sipariş")
d.box(10, 120, 150, 50, "Kasa / yönetim", "tablet · masa · menü")
d.box(300, 60, 170, 70, "Node.js + Express", "REST · Socket.io", accent=True)
d.wire([(160, 45), (230, 45), (230, 85), (300, 85)], both=True)
d.wire([(160, 145), (230, 145), (230, 105), (300, 105)], both=True)
d.box(560, 20, 190, 50, "MongoDB", "masa · sipariş · ürün")
d.box(560, 120, 190, 50, "Mutfak / kasa ekranı", "anlık güncelleme")
d.wire([(470, 85), (515, 85), (515, 45), (560, 45)])
d.wire([(470, 105), (515, 105), (515, 145), (560, 145)]).text(508, 132, "socket", "s", "end")
DIGI_DIAGRAM = d.render()

DIGI = dict(
    slug="project-order-management.html",
    cats=["sw"],
    title=("DigiTab Adisyon Sistemi", "DigiTab Order Management"),
    short=("DigiTab Adisyon Sistemi", "DigiTab Order Management"),
    year="2024",
    tags="React · Node.js · Socket.io",
    tags_en="React · Node.js · Socket.io",
    thumb=("digitab/logo.svg", "DigiTab logosu"),
    og="digitab/promo-02-cashier.webp",
    desc=("Restoran ve kafeler için gerçek zamanlı sipariş, masa ve menü yönetim sistemi.",
          "A real-time order, table and menu management system for restaurants and cafés."),
    meta=[(("Kategori", "Category"), b("Full-stack web uygulaması", "Full-stack web app")),
          ("Frontend", "React, TypeScript, Tailwind CSS"),
          ("Backend", "Node.js, Express, Socket.io"),
          (b("Veritabanı", "Database"), "MongoDB")],
    sections=[
        ("summary", ("Özet", "Summary"), "\n".join([
            B("p", "Kâğıt adisyonla çalışan bir işletmede sipariş garsondan mutfağa, oradan kasaya elden ele taşınıyor; bu da gecikme ve hata demek. DigiTab bu akışı dijitalleştiriyor: garson siparişi telefondan alıyor, mutfak ve kasa aynı anda görüyor, hesap tek tıkla çıkıyor.",
              "In a business running on paper tickets, an order travels by hand from waiter to kitchen to cashier, which means delays and mistakes. DigiTab digitises that flow: the waiter takes the order on a phone, the kitchen and cashier see it at the same moment, and the bill is one click away."),
        ])),
        ("diagram", ("Mimari", "Architecture"), DIGI_DIAGRAM),
        ("features", ("Özellikler", "Features"), spec([
            (b("Masa yönetimi", "Tables"), b("Masaların doluluk durumunu ve sipariş sürelerini anlık izleme", "Live table occupancy and order durations")),
            (b("Sipariş", "Orders"), b("Mobil/tablet üzerinden hızlı sipariş ve mutfağa anında iletim", "Fast ordering from phone/tablet with instant delivery to the kitchen")),
            (b("Menü", "Menu"), b("Ürün kategorileri, fiyatlandırma ve stok", "Product categories, pricing and stock")),
            (b("Adisyon", "Billing"), b("Tek tıkla hesap dökümü", "One-click bill")),
            (b("Raporlama", "Reports"), b("Günlük ciro ve en çok satan ürünler", "Daily revenue and best-selling items")),
            (b("Garson girişi", "Waiter access"), b("Yerel ağ adresi ve QR kod ile garson ekranına bağlanma", "Join the waiter screen via local network address and QR code")),
            (b("Dil", "Language"), b("TR / EN arayüz", "TR / EN interface")),
        ])),
        ("screens", ("Ekranlar", "Screens"), "\n".join([
            "{vid:digitab/promo.mp4|digitab/promo-02-cashier.webp|Tanıtım videosu|Promo video|Garson ekranından kasa paneline sipariş akışı.|Order flow from the waiter screen to the cashier panel.}",
            "{fig:digitab/promo-02-cashier.webp|Kasa paneli|Cashier panel|Masa durumu, adisyon ve otomatik hesaplanan toplam.|Table status, open bill and automatic total.|}",
            "{fig:digitab/promo-03-waiter.webp|Garson ekranı|Waiter screen|QR kodla açılan mobil ekranda masa seçimi, kategorili menü ve sipariş notu.|Table picker, categorised menu and order notes on the QR-launched mobile screen.|}",
            "{fig:digitab/promo-04-realtime.webp|Gerçek zamanlı senkronizasyon|Real-time sync|Garsonun gönderdiği sipariş kasa ekranına bir saniyenin altında düşer.|An order sent by the waiter reaches the cashier screen in under a second.|}",
            "{fig:digitab/promo-05-admin.webp|Yönetim|Admin|Kategori ve ürün yönetimi, açık / koyu tema.|Category and product management, light / dark theme.|}",
        ])),
        # TODO(Fatih): DigiTab reposu GitHub'da yok (eski sitedeki link 404 veriyordu). Repo açılınca bağlantı eklenecek.
    ],
)

PROJECTS = [CANBUS, GCS, ARM, QUAD, FC, CNC, DIGI]
