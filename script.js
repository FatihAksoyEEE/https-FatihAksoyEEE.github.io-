document.addEventListener('DOMContentLoaded', () => {

    // ─── SCROLL: NAVBAR SHRINK ───────────────────────────────────────────────
    const topnav = document.getElementById('topnav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            topnav.classList.add('scrolled');
        } else {
            topnav.classList.remove('scrolled');
        }
    });

    // ─── SMOOTH SCROLL ───────────────────────────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = topnav.offsetHeight + 16;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // ─── THEME TOGGLE ────────────────────────────────────────────────────────
    const themeBtn = document.getElementById('themeBtn');
    const sunIcon = document.getElementById('sunIcon');
    const moonIcon = document.getElementById('moonIcon');
    const html = document.documentElement;

    const savedTheme = localStorage.getItem('theme') || 'dark';
    applyTheme(savedTheme);

    themeBtn.addEventListener('click', () => {
        const current = html.getAttribute('data-theme');
        applyTheme(current === 'dark' ? 'light' : 'dark');
    });

    function applyTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        if (theme === 'dark') {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        } else {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        }
    }

    // ─── LANGUAGE TOGGLE ─────────────────────────────────────────────────────
    const langBtn = document.getElementById('langBtn');
    const langLabel = document.getElementById('langLabel');

    let currentLang = localStorage.getItem('lang') || 'tr';
    applyLang(currentLang);

    langBtn.addEventListener('click', () => {
        currentLang = currentLang === 'tr' ? 'en' : 'tr';
        applyLang(currentLang);
    });

    function applyLang(lang) {
        localStorage.setItem('lang', lang);
        langLabel.textContent = lang.toUpperCase();

        // Translate all elements that have data-tr and data-en
        document.querySelectorAll('[data-tr]').forEach(el => {
            const text = el.getAttribute('data-' + lang);
            if (text) el.innerHTML = text;
        });

        // Update html lang attribute
        document.documentElement.lang = lang;
    }

    // ─── SCROLL ANIMATIONS ───────────────────────────────────────────────────
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.hero-content, .portrait-container, .glass-header, .about-text, .project-card, .social-links, .cv-button').forEach(el => {
        el.classList.add('hidden');
        observer.observe(el);
    });
});
