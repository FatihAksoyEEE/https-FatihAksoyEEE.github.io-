# fatihaksoy.com Yenileme Planı

Amaç: Siteyi "fütüristik AI şablonu" görünümünden çıkarıp, gerçek mühendislik işini kanıtlarla gösteren profesyonel bir portföye dönüştürmek.

- **Tasarım yönü:** A. Mühendislik defteri / datasheet (kesinleşmedi, değişirse bu bölüm güncellenecek)
- **Teknoloji:** Düz HTML + CSS + JS, GitHub Pages (`main` dalı, `CNAME` → fatihaksoy.com). Astro'ya geçiş opsiyonel (bkz. Faz 6).
- **Çalışma kuralı:** Her faz localhost'ta (`python3 -m http.server 8000`) yapılır ve kontrol edilir. Commit ve push yalnızca onaydan sonra yapılır.

---

## Faz 0: Acil düzeltmeler (canlı site)

Tasarım değişmeden, mevcut sitedeki kırıklar giderilir.

- [ ] İHA görseli: `assets/images/İha.png` repoda yok (404). Orijinali bulunacak ya da geçici bir görsel konacak.
- [ ] Karışık görseller düzeltilecek:
  - `robot-arm.png` aslında yer istasyonu çantası → `control-station.png` olarak yeniden adlandırılacak.
  - `drone.png` aslında robot kol render'ı → `robot-arm.png` olarak yeniden adlandırılacak.
  - `index.html` ve ilgili proje sayfalarındaki referanslar güncellenecek.
- [ ] CV butonunun HTML'deki varsayılan metni TR yapılacak ("DOWNLOAD CV" → "CV İNDİR").
- [ ] Repodan `.DS_Store` dosyaları çıkarılacak (`git rm --cached .DS_Store assets/.DS_Store`).

## Faz 1: Tasarım sistemi

Yeni `styles.css`, tüm sayfaların paylaştığı tek bir dosya olarak sıfırdan yazılır.

- [ ] **Renk token'ları** (`:root` değişkenleri):
  - Açık tema: kırık beyaz kâğıt zemin, koyu grafit metin, ince milimetrik grid çizgileri.
  - Koyu tema: grafit zemin, aynı grid daha soluk.
  - Tek vurgu rengi: sinyal turuncusu (alternatif: PCB yeşili).
  - `prefers-color-scheme` desteği ve elle tema değiştirme butonu.
- [ ] **Tipografi:** IBM Plex Sans (metin) ve IBM Plex Mono (etiket, pin, değer, tarih).
  - Orbitron, Rajdhani ve Michroma kaldırılacak.
  - Her şeyi BÜYÜK HARF yapma alışkanlığı bırakılacak, büyük harf sadece küçük mono etiketlerde kullanılacak.
- [ ] **Kaldırılacak efektler:** Gradient metin, glow gölgeler, glassmorphism (`.glass-header`), hover'da zıplayan kartlar, global `* { transition }`.
- [ ] **Bileşenler:** Header/nav, bölüm başlığı (`01 / Hakkında` tarzı), proje listesi satırı, özellik tablosu (spec table), figür ve altyazı, buton/link, footer.
- [ ] **Hareket:** Minimal geçişler. `prefers-reduced-motion` desteği olacak.

## Faz 2: Ana sayfa (`index.html`)

- [ ] **Header:** İsim, sade nav (Hakkında · Projeler · İletişim), TR/EN ve tema butonları. Mobilde çalışan bir menü (hamburger ya da kompakt satır).
- [ ] **Giriş:** Portre (defter kâğıdına karakalem çizim, tasarım yönünün çıkış noktası), isim, tek cümlelik tanım, CV ve iletişim linkleri.
- [ ] **Hakkında:** Okul/sınıf, odak alanları, kullanılan araçlar (KiCad/Altium, STM32CubeIDE vb.) ve kısa bir zaman çizelgesi.
- [ ] **Projeler:** Kart grid'i yerine numaralı liste.
  Örnek: `01 — STM32 Flight Controller · 2025 · PCB / Firmware`, yanında küçük bir görsel.
- [ ] **İletişim:** E-posta, GitHub, LinkedIn (yeni), YouTube, Instagram (ikinci planda).
- [ ] JS kapalıyken içerik görünür kalacak (`.hidden` mantığı kaldırılacak).

## Faz 3: Proje sayfaları (datasheet şablonu)

Tek bir ortak şablon hazırlanır ve tüm projeler ona taşınır.

**Şablon bölümleri:**
1. Başlık bloğu: proje adı, yıl, rol, etiketler, GitHub linki
2. Özet: problem ve çözüm, 2–3 cümle
3. Blok diyagram
4. Özellik tablosu: MCU, sensörler, haberleşme, güç vb.
5. Donanım: şema ve PCB görselleri
6. Yazılım / firmware
7. Sonuçlar ve öğrenilenler
8. Linkler: repo, video, dokümanlar

**Sayfalar:**
- [ ] `project-cnc.html`: Mevcut içerik şablona taşınacak (dolu sayfa, ilk prototip bu olacak).
- [ ] `project-order-management.html` (Digitab): Mevcut içerik şablona taşınacak.
- [ ] `project-flight-controller.html`: `ESP32_Drone` / STM32 kaynaklarından doldurulacak.
- [ ] `project-uav.html`: Doldurulacak.
- [ ] `project-robot-arm.html`: `RoboArm` reposunun README'sinden doldurulacak.
- [ ] `project-control-station.html`: `Ground-Control-System` reposunun README'sinden doldurulacak.
- [ ] **Yeni:** `project-canbus-sniffer.html`, CANable ile tersine mühendislikle RPM çözme.
- [ ] **Opsiyonel:** SnapRoute.

> Not: Ölçüm ve sonuç değerleri uydurulmayacak. README'lerde olmayan bilgiler Fatih'ten alınacak, eksikler `TODO` olarak işaretlenecek.

## Faz 4: İçerik ve görseller

- [ ] Stok render'lar yerine gerçek fotoğraflar kullanılacak: tezgâh, lehim, test ve ekipman çekimleri.
- [ ] YouTube videoları ilgili proje sayfalarına gömülecek (lite embed ile, sayfayı yavaşlatmadan).
- [ ] `assets/images/digitab/` içindeki boşluklu WhatsApp dosya adları düzgün isimlerle değiştirilecek (`digitab-01.jpg` …).
- [ ] TR/EN metinleri gözden geçirilecek. Varsayılan dil HTML'de TR olacak.

## Faz 5: Performans, SEO, erişilebilirlik

- [ ] **Görseller:** WebP'ye dönüştürme ve uygun boyutlandırma (`portrait.png` 2.3 MB, CNC görselleri 0.5–1.4 MB). `loading="lazy"`, `width`/`height` attribute'ları eklenecek.
- [ ] **Fontlar:** Sadece kullanılan ağırlıklar yüklenecek, `font-display: swap`.
- [ ] **SEO:** Her sayfaya `<meta name="description">`, Open Graph/Twitter kartları (LinkedIn/WhatsApp önizleme görseli), canonical link, favicon, `sitemap.xml`, `robots.txt`.
- [ ] **Erişilebilirlik:** İkon butonlarına `aria-label`, anlamlı `alt` metinleri, klavye ile gezinme ve görünür focus, kontrast kontrolü (WCAG AA).
- [ ] **Kontrol:** Lighthouse (mobil + masaüstü), hedef: tüm skorlar 90+.

## Faz 6: Bakım (opsiyonel)

- [ ] Header/footer tekrarını azaltmak. Seçenekler:
  - Düz HTML'de kalıp ortak parçaları basit bir JS include ile yüklemek, veya
  - Astro'ya geçmek (GitHub Pages ile sorunsuz çalışır, bileşen ve markdown tabanlı proje sayfaları sağlar).
- [ ] Karar Faz 3 sonunda verilecek.

---

## Uygulama sırası

1. **Faz 0** → hemen, ayrı commit. Canlı siteyi kurtarır.
2. **Faz 1 + Faz 2 + CNC sayfası** → prototip. localhost'ta gözden geçirilir, onay alınır.
3. **Faz 3** (kalan sayfalar) + **Faz 4** → içerik geldikçe.
4. **Faz 5** → yayın öncesi son geçiş.
5. Yayın: `main`'e push edilir, fatihaksoy.com üzerinde kontrol edilir.

## Açık sorular

- [ ] Tasarım yönü A olarak mı kesinleşiyor? Vurgu rengi turuncu mu, yeşil mi?
- [ ] İHA görselinin orijinali var mı?
- [ ] LinkedIn profil linki nedir?
- [ ] Gerçek proje fotoğrafları var mı / çekilebilir mi?
- [ ] Boş projelerin sonuç ve ölçüm değerleri (Flight Controller, İHA, Robot Kol, Kontrol İstasyonu).
- [ ] CANable ve SnapRoute siteye eklenecek mi?
