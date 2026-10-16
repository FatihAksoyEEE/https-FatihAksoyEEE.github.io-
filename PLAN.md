# fatihaksoy.com Yenileme Planı

Amaç: Siteyi "fütüristik AI şablonu" görünümünden çıkarıp, gerçek mühendislik işini kanıtlarla gösteren profesyonel bir portföye dönüştürmek.

- **Tasarım yönü:** A. Mühendislik defteri / datasheet (uygulandı; vurgu rengi sinyal turuncusu)
- **Teknoloji:** Düz HTML + CSS + JS, GitHub Pages (`main` dalı, `CNAME` → fatihaksoy.com). Astro'ya geçiş opsiyonel (bkz. Faz 6).
- **Çalışma kuralı:** Her faz localhost'ta (`python3 -m http.server 8000`) yapılır ve kontrol edilir. Commit ve push yalnızca onaydan sonra yapılır.

---

## Faz 0: Acil düzeltmeler (canlı site)

Tasarım değişmeden, mevcut sitedeki kırıklar giderilir.

- [x] İHA görseli: `assets/images/İha.png` repoda yok (404). Orijinal bulunamadı; yerine ESP32_Drone reposundaki kartın 3D render'ı kondu.
- [x] Karışık görseller düzeltilecek:
  - `robot-arm.png` aslında yer istasyonu çantası → `control-station.png` olarak yeniden adlandırılacak.
  - `drone.png` aslında robot kol render'ı → `robot-arm.png` olarak yeniden adlandırılacak.
  - `index.html` ve ilgili proje sayfalarındaki referanslar güncellenecek.
- [x] CV butonunun HTML'deki varsayılan metni TR yapılacak ("DOWNLOAD CV" → "CV İNDİR").
- [x] Repodan `.DS_Store` dosyaları çıkarılacak (`git rm --cached .DS_Store assets/.DS_Store`).

## Faz 1: Tasarım sistemi

Yeni `styles.css`, tüm sayfaların paylaştığı tek bir dosya olarak sıfırdan yazılır.

- [x] **Renk token'ları** (`:root` değişkenleri):
  - Açık tema: kırık beyaz kâğıt zemin, koyu grafit metin, ince milimetrik grid çizgileri.
  - Koyu tema: grafit zemin, aynı grid daha soluk.
  - Tek vurgu rengi: sinyal turuncusu (alternatif: PCB yeşili).
  - `prefers-color-scheme` desteği ve elle tema değiştirme butonu.
- [x] **Tipografi:** IBM Plex Sans (metin) ve IBM Plex Mono (etiket, pin, değer, tarih).
  - Orbitron, Rajdhani ve Michroma kaldırılacak.
  - Her şeyi BÜYÜK HARF yapma alışkanlığı bırakılacak, büyük harf sadece küçük mono etiketlerde kullanılacak.
- [x] **Kaldırılacak efektler:** Gradient metin, glow gölgeler, glassmorphism (`.glass-header`), hover'da zıplayan kartlar, global `* { transition }`.
- [x] **Bileşenler:** Header/nav, bölüm başlığı (`01 / Hakkında` tarzı), proje listesi satırı, özellik tablosu (spec table), figür ve altyazı, buton/link, footer.
- [x] **Hareket:** Minimal geçişler. `prefers-reduced-motion` desteği olacak.

## Faz 2: Ana sayfa (`index.html`)

- [x] **Header:** İsim, sade nav (Hakkında · Projeler · İletişim), TR/EN ve tema butonları. Mobilde çalışan bir menü (hamburger ya da kompakt satır).
- [x] **Giriş:** Portre (defter kâğıdına karakalem çizim, tasarım yönünün çıkış noktası), isim, tek cümlelik tanım, CV ve iletişim linkleri.
- [x] **Hakkında:** Odak alanları ve araçlar (repolardan: KiCad, PlatformIO, PyQt6, React/Electron…) eklendi.
- [ ] Okul/sınıf ve zaman çizelgesi → bilgi bekleniyor (`index.html` içinde `TODO(Fatih)` yorumu var).
- [x] **Projeler:** Kart grid'i yerine numaralı liste.
  Örnek: `01 — STM32 Flight Controller · 2025 · PCB / Firmware`, yanında küçük bir görsel.
- [x] **İletişim:** E-posta, GitHub, YouTube, Instagram, CV.
- [ ] LinkedIn → profil linki bekleniyor (`TODO(Fatih)` yorumu var).
- [x] JS kapalıyken içerik görünür kalacak (`.hidden` mantığı kaldırılacak).

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
- [x] `project-cnc.html`: Mevcut içerik şablona taşınacak (dolu sayfa, ilk prototip bu olacak).
- [x] `project-order-management.html` (Digitab): Mevcut içerik şablona taşınacak.
- [~] `project-flight-controller.html`: Şablona taşındı, kart render'ı ve görünen özellikler yazıldı. Bu kartın reposu yok; şema, özellik tablosu ve test sonuçları bekleniyor.
- [x] `project-uav.html`: **ESP32 Quadcopter** sayfası oldu (`ESP32_Drone` reposu + KiCad şeması). Eski sayfadaki "otonom uçuş, görüntü işleme, OpenCV" iddiaları hiçbir kaynakta yok, kaldırıldı.
- [x] `project-robot-arm.html`: `RoboArm` reposundan dolduruldu. Stok robot render'ı kaldırıldı. Eski "Arduino, inverse kinematics" bilgisi repoyla çeliştiği için düzeltildi.
- [x] `project-control-station.html`: `Ground-Control-System` kaynak kodundan dolduruldu (paket formatı dahil). Eski "Qt, C++, MAVLink" bilgisi kodla çeliştiği için düzeltildi. Sana ait olmayan stok yer istasyonu fotoğrafı kaldırıldı.
- [x] **Yeni:** `project-canbus-sniffer.html`, CANable ile tersine mühendislikle RPM çözme.
- [ ] **Opsiyonel:** SnapRoute → eklenmedi, karar bekleniyor.

> Not: Ölçüm ve sonuç değerleri uydurulmayacak. README'lerde olmayan bilgiler Fatih'ten alınacak, eksikler `TODO` olarak işaretlenecek.

## Faz 4: İçerik ve görseller

- [x] Stok render'lar kaldırıldı; yerine repolardaki gerçek tasarım çıktıları (KiCad şema/PCB, arayüz ekranları) ve blok diyagramlar kondu.
- [ ] Tezgâh, lehim ve test fotoğrafları → çekilmesi bekleniyor.
- [ ] YouTube videoları → kanalda herkese açık video bulunamadı; video yayınlanınca eklenecek.
- [x] `assets/images/digitab/` içindeki boşluklu WhatsApp dosya adları düzgün isimlerle değiştirilecek (`digitab-01.jpg` …).
- [x] TR/EN metinleri gözden geçirilecek. Varsayılan dil HTML'de TR olacak.

## Faz 5: Performans, SEO, erişilebilirlik

- [x] **Görseller:** WebP'ye dönüştürme ve uygun boyutlandırma (`portrait.png` 2.3 MB, CNC görselleri 0.5–1.4 MB). `loading="lazy"`, `width`/`height` attribute'ları eklenecek.
- [x] **Fontlar:** Sadece kullanılan ağırlıklar yüklenecek, `font-display: swap`.
- [x] **SEO:** Her sayfaya `<meta name="description">`, Open Graph/Twitter kartları (LinkedIn/WhatsApp önizleme görseli), canonical link, favicon, `sitemap.xml`, `robots.txt`.
- [x] **Erişilebilirlik:** İkon butonlarına `aria-label`, anlamlı `alt` metinleri, klavye ile gezinme ve görünür focus, kontrast kontrolü (WCAG AA).
- [~] **Kontrol:** Bu makinede Chrome/Node olmadığı için Lighthouse çalıştırılamadı. Yerine yapılanlar: WebKit ile 360/390/1280 px ekran görüntüleri (açık/koyu, TR/EN), yatay taşma ölçümü, HTML yapı/çapa/link kontrolü, WCAG kontrast hesabı (tüm metin renkleri ≥ 4.5:1). Yayından sonra PageSpeed Insights ile ölçülmeli.

## Faz 6: Bakım (opsiyonel)

- [x] Header/footer tekrarını azaltmak. **Karar:** Düz HTML'de kalındı (GitHub Pages'te build adımı yok). Sayfalar `tools/build/build.py` ile üretiliyor; ortak parçalar `common.py`, içerik `projects.py` içinde. Değerlendirilen seçenekler:
  - Düz HTML'de kalıp ortak parçaları basit bir JS include ile yüklemek, veya
  - Astro'ya geçmek (GitHub Pages ile sorunsuz çalışır, bileşen ve markdown tabanlı proje sayfaları sağlar).
- [x] Karar verildi (yukarıda).

---

## Uygulama sırası

1. **Faz 0** → hemen, ayrı commit. Canlı siteyi kurtarır.
2. **Faz 1 + Faz 2 + CNC sayfası** → prototip. localhost'ta gözden geçirilir, onay alınır.
3. **Faz 3** (kalan sayfalar) + **Faz 4** → içerik geldikçe.
4. **Faz 5** → yayın öncesi son geçiş.
5. Yayın: `main`'e push edilir, fatihaksoy.com üzerinde kontrol edilir. → **Onay bekliyor** (commit'ler yerelde, push yapılmadı).

## Açık sorular

- [ ] Okul, sınıf ve kısa zaman çizelgesi (Hakkında bölümü)
- [ ] LinkedIn profil linki
- [ ] Proje yılları doğru mu? Repo tarihleri esas alındı: CAN 2026, GCS 2026, Robot Kol 2026, ESP32 Quadcopter 2025. CNC, STM32 FC ve DigiTab için eski sitedeki 2024 korundu.
- [ ] STM32 uçuş kontrol kartı: MCU modeli, IMU, şema/PCB görselleri, repo
- [ ] DigiTab reposu GitHub'da yok (eski sitedeki link 404 veriyordu, kaldırıldı). Açılacak mı?
- [ ] Robot kol arayüz görüntüsündeki "FABRI CREATOR" markası sana mı ait? Değilse görsel değiştirilmeli.
- [ ] Gerçek proje fotoğrafları (tezgâh, lehim, test)
- [ ] SnapRoute siteye eklenecek mi?
