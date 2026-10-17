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
- [x] Okul/sınıf ve eğitim-staj çizelgesi yeni CV'den eklendi.
- [x] **Projeler:** Kart grid'i yerine numaralı liste.
  Örnek: `01 — STM32 Flight Controller · 2025 · PCB / Firmware`, yanında küçük bir görsel.
- [x] **İletişim:** E-posta, GitHub, YouTube, Instagram, CV.
- [x] LinkedIn eklendi (CV'deki link). CV linkleri `Mehmet_Fatih_Aksoy_CV_TR-EN.pdf` dosyasına bağlandı.
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
- [x] `project-flight-controller.html`: Şablona taşındı, kart render'ı ve görünen özellikler yazıldı. Eksik bilgiler (şema, özellik tablosu, test sonuçları) Fatih'ten bekleniyor → Faz 12.
- [x] `project-uav.html`: **ESP32 Quadcopter** sayfası oldu (`ESP32_Drone` reposu + KiCad şeması). Eski sayfadaki "otonom uçuş, görüntü işleme, OpenCV" iddiaları hiçbir kaynakta yok, kaldırıldı.
- [x] `project-robot-arm.html`: `RoboArm` reposundan dolduruldu. Stok robot render'ı ve arayüz görüntüsü kaldırıldı; yerine kolun kendi 3D CAD modelinden iki görünüm kondu. Eski "Arduino, inverse kinematics" bilgisi repoyla çeliştiği için düzeltildi.
- [x] `project-control-station.html`: `Ground-Control-System` kaynak kodundan dolduruldu (paket formatı dahil). Eski "Qt, C++, MAVLink" bilgisi kodla çeliştiği için düzeltildi. Sana ait olmayan stok yer istasyonu fotoğrafı kaldırıldı.
- [x] **Yeni:** `project-canbus-sniffer.html`, CANable ile tersine mühendislikle RPM çözme.
- [x] **Opsiyonel:** SnapRoute → **Karar (Ekim 2026): eklenmeyecek.**

> Not: Ölçüm ve sonuç değerleri uydurulmayacak. README'lerde olmayan bilgiler Fatih'ten alınacak, eksikler `TODO` olarak işaretlenecek.

## Faz 4: İçerik ve görseller

- [x] Stok render'lar kaldırıldı; yerine repolardaki gerçek tasarım çıktıları (KiCad şema/PCB, arayüz ekranları) ve blok diyagramlar kondu.
- [x] Tezgâh, lehim ve test fotoğrafları → Faz 12'ye taşındı (Fatih'ten bekleniyor).
- [x] YouTube videoları → Faz 12'ye taşındı. Ekim 2026'da tekrar kontrol edildi: kanalda hâlâ herkese açık video yok.
- [x] `assets/images/digitab/` içindeki boşluklu WhatsApp dosya adları düzgün isimlerle değiştirilecek (`digitab-01.jpg` …).
- [x] TR/EN metinleri gözden geçirilecek. Varsayılan dil HTML'de TR olacak.

## Faz 5: Performans, SEO, erişilebilirlik

- [x] **Görseller:** WebP'ye dönüştürme ve uygun boyutlandırma (`portrait.png` 2.3 MB, CNC görselleri 0.5–1.4 MB). `loading="lazy"`, `width`/`height` attribute'ları eklenecek.
- [x] **Fontlar:** Sadece kullanılan ağırlıklar yüklenecek, `font-display: swap`.
- [x] **SEO:** Her sayfaya `<meta name="description">`, Open Graph/Twitter kartları (LinkedIn/WhatsApp önizleme görseli), canonical link, favicon, `sitemap.xml`, `robots.txt`.
- [x] **Erişilebilirlik:** İkon butonlarına `aria-label`, anlamlı `alt` metinleri, klavye ile gezinme ve görünür focus, kontrast kontrolü (WCAG AA).
- [x] **Kontrol:** Lighthouse yerelde çalıştırılamadı (Node yok). Yerine yapılanlar: WebKit ile 360/390/1280 px ekran görüntüleri (açık/koyu, TR/EN), yatay taşma ölçümü, HTML yapı/çapa/link kontrolü, WCAG kontrast hesabı (tüm metin renkleri ≥ 4.5:1). Yayından sonra PageSpeed Insights ile ölçülmeli (Faz 9). Ekim 2026: Playwright/Chromium ile 34 sayfa açılışında konsol hatası, 4xx kaynak ve 360/1280 px yatay taşma kontrolü temiz.

## Faz 6: Bakım (opsiyonel)

- [x] Header/footer tekrarını azaltmak. **Karar:** Düz HTML'de kalındı (GitHub Pages'te build adımı yok). Sayfalar `tools/build/build.py` ile üretiliyor; ortak parçalar `common.py`, içerik `projects.py` içinde. Değerlendirilen seçenekler:
  - Düz HTML'de kalıp ortak parçaları basit bir JS include ile yüklemek, veya
  - Astro'ya geçmek (GitHub Pages ile sorunsuz çalışır, bileşen ve markdown tabanlı proje sayfaları sağlar).
- [x] Karar verildi (yukarıda).

## Faz 7: DigiTab görselleri

- [x] Eski DigiTab ekran görüntüleri (`assets/img/digitab/tablet-*`, `mobile-*`) tamamen kaldırıldı.
- [x] Yerine `~/Developer/DigiTab/Promo` içindeki tanıtım görselleri (WebP'ye dönüştürülerek) ve tanıtım videosu kondu.
- [x] Ana sayfadaki proje satırı için DigiTab logosu tasarlandı (`assets/img/digitab/logo.svg`). Sosyal medya önizlemesi (og:image) için tanıtım görseli kullanılıyor.

## Faz 8: Yayın öncesi

- [x] Değişiklikler commit'lenip `main`'e push edildi (17 Ekim 2026); fatihaksoy.com üzerinde TR, `/en/`, 404 ve eski CV adresi kontrol edildi.
  - GitHub hesabındaki ödeme sorunu yüzünden ilk CI çalışması başlamamıştı; Fatih sorunu çözdü, kontrol geçiyor.
- [x] Eski CV linki (`assets/FatihAksoy_CV.pdf`) kırılmasın diye güncel CV eski adla da bırakıldı.
- [x] Videolar `ffmpeg` ile sıkıştırıldı (H.264, CRF 28, 1280 px, faststart): `demo-bench.mp4` 9,7 MB → 0,45 MB, `demo-tour.mp4` 2,3 → 0,14 MB, DigiTab `promo.mp4` 3,7 → 0,63 MB. Ekran kaydı olduğu için 720p yerine 1280 px genişlik korundu; kalite kare karşılaştırmasıyla kontrol edildi. DigiTab videosunun kapanış kartındaki "macOS masaüstü uygulaması" rozet satırı silindi.
- [x] `404.html` eklendi ("Sinyal yok.", TR + EN, mutlak yollar sayesinde `/en/...` altında da çalışır, `noindex`).

## Faz 9: SEO ve görünürlük

- [x] İngilizce sayfalar `/en/` altında üretiliyor; her sayfada `hreflang` (tr, en, x-default) ve dile göre canonical/og etiketleri var. Her dilin sayfasında yalnızca o dilin metni kalıyor (build sırasında diğer dil çıkarılıyor). Dil butonu artık karşı dildeki sayfaya giden bir bağlantı; JS gerekmiyor. Diyagram etiketleri ve görsel alt metinleri de çevrildi. `sitemap.xml` iki dili `xhtml:link` ile listeliyor.
- [x] JSON-LD: ana sayfada `Person` (isim, üniversite, uzmanlıklar, `sameAs`: GitHub, LinkedIn, YouTube, Instagram), proje sayfalarında yazara bağlı `CreativeWork`.
- [x] Yayından sonra Lighthouse ölçümü (17 Ekim 2026, canlı site; PageSpeed API kotası dolu olduğu için Lighthouse 12 yerelde çalıştırıldı). İlk ölçümde mobil performans ana sayfada 78'di (LCP 4,2 s); Google Fonts render'ı blokluyordu ve ana sayfa görselleri büyüktü. Düzeltmeler: fontlar `assets/fonts` altına alındı (preload), ana sayfa için 336 px görsel kopyaları build'de üretiliyor, dil bağlantısının erişilebilir adı düzeltildi. Sonuç (performans / erişilebilirlik / en iyi uygulamalar / SEO):
  - `/` mobil 99 / 100 / 100 / 100 (LCP 2,2 s), masaüstü 100 / 100 / 100 / 100
  - `/en/project-canbus-sniffer.html` mobil 98, masaüstü 100; diğerleri 100
  - `/project-order-management.html` mobil ve masaüstü 100 / 100 / 100 / 100
  - Kalan uyarılar: önbellek süresi (GitHub Pages'te değiştirilemiyor) ve proje sayfalarındaki şema görsellerinin boyutu (büyütme için bilerek büyük).

## Faz 10: Kullanılabilirlik

- [x] Proje sayfalarında önceki / sonraki proje linkleri (zaten mevcut, `build.py` içindeki `pager`).
- [x] Şekillere tıklayınca `<dialog>` içinde büyütme (Esc / arka plana tıklama ile kapanır; JS yokken görsel yeni sayfada açılır).
- [x] Ana sayfada filtre: Tümü · PCB · Firmware · Yazılım (kategoriler `projects.py` içinde `cats`). JS yokken gizli kalır, liste tam görünür.

## Faz 11: Bakım ve ölçüm

- [x] GitHub Actions (`.github/workflows/check.yml`): her push/PR'da `build.py` çalıştırılıp çıktının repodakiyle aynı olduğu doğrulanıyor, `lychee` ile site içi kırık bağlantı kontrolü yapılıyor.
- [x] Çerezsiz ziyaretçi istatistiği (GoatCounter) hazır ama **kapalı**: Fatih şimdilik istemedi (Ekim 2026). Açmak için `tools/build/common.py` içindeki `GOATCOUNTER` değişkenine site kodunu yazıp build almak yeterli; CV indirme bağlantıları `data-goatcounter-click="cv-indir"` ile zaten işaretli.

## Faz 12: İçerik (Fatih'ten gelecek)

Bu maddeler site tarafında yapılacak bir iş değil; içerik gelince eklenecek. `[-]` = dış girdi bekleniyor (Ekim 2026'da soruldu: henüz yok).

- [-] Tezgâh, lehim ve test fotoğrafları.
- [-] STM32 uçuş kontrol kartı: MCU, IMU, şema/PCB görselleri, repo.
- [-] DigiTab reposunun GitHub'da açılması (açılınca proje sayfasına bağlantı eklenecek; `projects.py` içinde TODO var).
- [-] YouTube videoları (yayınlanınca ilgili proje sayfalarına eklenecek).
- [-] Opsiyonel: "Notlar / Blog" bölümü (örn. CAN hattını çözme süreci). Yazıların Fatih'in kendi anlatımıyla gelmesi gerekiyor.

---

## Uygulama sırası

1. **Faz 0** → hemen, ayrı commit. Canlı siteyi kurtarır.
2. **Faz 1 + Faz 2 + CNC sayfası** → prototip. localhost'ta gözden geçirilir, onay alınır.
3. **Faz 3** (kalan sayfalar) + **Faz 4** → içerik geldikçe.
4. **Faz 5** → yayın öncesi son geçiş.
5. Yayın: `main`'e push edilir, fatihaksoy.com üzerinde kontrol edilir. → **Yayında** (17 Ekim 2026).

## Açık sorular

- [x] Proje yılları doğru mu? CAN 2026, GCS 2026, Robot Kol 2026, ESP32 Quadcopter 2025, CNC / STM32 FC / DigiTab 2024. **Fatih onayladı (Ekim 2026).**
- [-] STM32 uçuş kontrol kartı: MCU modeli, IMU, şema/PCB görselleri, repo → Faz 12
- [-] DigiTab reposu GitHub'da yok (Ekim 2026'da tekrar kontrol edildi: 404) → Faz 12
- [-] Gerçek proje fotoğrafları (tezgâh, lehim, test) → Faz 12
- [x] SnapRoute siteye eklenecek mi? → Hayır.
