// Tema ve dil tercihleri. İlk değerler <head> içindeki küçük betikle,
// sayfa çizilmeden önce uygulanır; burada yalnızca butonlar bağlanır.
(function () {
    const root = document.documentElement;

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
        const label = root.lang === 'en'
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
    }

    // ─── Dil ─────────────────────────────────────────────────────────────────
    const langBtn = document.getElementById('langBtn');
    const titles = {
        tr: document.title,
        en: document.querySelector('meta[name="title-en"]')?.content || document.title,
    };

    function applyLang(lang) {
        root.lang = lang;
        document.title = titles[lang];
        if (langBtn) {
            const other = lang === 'tr' ? 'en' : 'tr';
            langBtn.textContent = other.toUpperCase();
            langBtn.setAttribute('aria-label', lang === 'tr' ? 'Switch to English' : 'Türkçeye geç');
            langBtn.title = langBtn.getAttribute('aria-label');
            langBtn.lang = other;
        }
        syncThemeBtn();
    }

    if (langBtn) {
        langBtn.addEventListener('click', () => {
            const next = root.lang === 'tr' ? 'en' : 'tr';
            store('lang', next);
            applyLang(next);
        });
    }

    applyLang(root.lang === 'en' ? 'en' : 'tr');
})();
