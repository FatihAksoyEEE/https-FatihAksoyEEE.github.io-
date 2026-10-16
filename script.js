// Tema tercihi, görsel büyütme ve proje filtresi. Dil adresle belirlenir (/ ve /en/);
// tema ilk değeri <head> içindeki küçük betikle, sayfa çizilmeden önce uygulanır.
(function () {
    const root = document.documentElement;
    const en = root.lang === 'en';

    function store(key, value) {
        try { localStorage.setItem(key, value); } catch (e) { /* gizli sekme vb. */ }
    }

    // ─── Tema ────────────────────────────────────────────────────────────────
    const themeBtn = document.getElementById('themeBtn');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

    function currentTheme() {
        return root.dataset.theme || (prefersDark.matches ? 'dark' : 'light');
    }

    function syncThemeBtn() {
        if (!themeBtn) return;
        const next = currentTheme() === 'dark' ? 'light' : 'dark';
        const label = en
            ? (next === 'dark' ? 'Switch to dark theme' : 'Switch to light theme')
            : (next === 'dark' ? 'Koyu temaya geç' : 'Açık temaya geç');
        themeBtn.setAttribute('aria-label', label);
        themeBtn.title = label;
    }

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const next = currentTheme() === 'dark' ? 'light' : 'dark';
            root.dataset.theme = next;
            store('theme', next);
            syncThemeBtn();
        });
        syncThemeBtn();
    }

    // ─── Görsel büyütme ──────────────────────────────────────────────────────
    // Şekillerdeki bağlantılar JS yokken görseli yeni sayfada açar; JS varken <dialog> içinde.
    const figLinks = document.querySelectorAll('.fig > a[href]');
    if (figLinks.length && typeof HTMLDialogElement === 'function') {
        const dlg = document.createElement('dialog');
        dlg.className = 'lightbox';
        dlg.setAttribute('aria-label', en ? 'Enlarged image' : 'Büyütülmüş görsel');
        dlg.innerHTML = '<button type="button" class="ctrl-btn lightbox-close"></button>' +
            '<img alt=""><p class="lightbox-cap"></p>';
        const closeBtn = dlg.querySelector('.lightbox-close');
        closeBtn.textContent = en ? 'Close ✕' : 'Kapat ✕';
        const big = dlg.querySelector('img');
        const cap = dlg.querySelector('.lightbox-cap');
        document.body.appendChild(dlg);

        figLinks.forEach((a) => {
            a.addEventListener('click', (e) => {
                if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
                e.preventDefault();
                const img = a.querySelector('img');
                const fc = a.parentElement.querySelector('figcaption');
                big.src = a.href;
                big.alt = img ? img.alt : '';
                // "Şekil 3" etiketi ile açıklama ayrı elemanlarda; aralarına ayraç koy
                let text = '';
                if (fc) {
                    const rest = fc.cloneNode(true);
                    const label = rest.querySelector('.label');
                    if (label) label.remove();
                    text = (label ? label.textContent + ' · ' : '') + rest.textContent.trim();
                }
                cap.textContent = text;
                dlg.showModal();
            });
        });
        closeBtn.addEventListener('click', () => dlg.close());
        // Görselin dışına (arka plana) tıklayınca kapan
        dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
        dlg.addEventListener('close', () => { big.removeAttribute('src'); });
    }

    // ─── Proje filtresi ──────────────────────────────────────────────────────
    const filter = document.querySelector('.filter');
    if (filter) {
        const buttons = filter.querySelectorAll('button');
        const items = document.querySelectorAll('.project-list > li');
        filter.hidden = false;
        buttons.forEach((btn) => {
            btn.addEventListener('click', () => {
                const cat = btn.dataset.cat;
                buttons.forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
                items.forEach((li) => {
                    li.hidden = !!cat && !li.dataset.cats.split(' ').includes(cat);
                });
            });
        });
    }
})();
