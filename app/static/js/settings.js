let currentLanguage = localStorage.getItem('language') || 'ru';
let currentTheme = localStorage.getItem('theme') || 'dark';

function loadLanguage() {
    fetch(`/static/i18n/${currentLanguage}.json`)
        .then(response => response.json())
        .then(translations => {
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (translations[key]) {
                    if (el.tagName === 'INPUT' && el.placeholder) {
                        el.placeholder = translations[key];
                    } else {
                        el.textContent = translations[key];
                    }
                }
            });
            document.title = translations.app_name;
        });
}

function loadTheme() {
    const themeLink = document.getElementById('theme-style');
    if (!themeLink) {
        const link = document.createElement('link');
        link.id = 'theme-style';
        link.rel = 'stylesheet';
        link.href = `/static/css/themes/${currentTheme}.css`;
        document.head.appendChild(link);
    } else {
        themeLink.href = `/static/css/themes/${currentTheme}.css`;
    }
    document.body.setAttribute('data-theme', currentTheme);
}

function openSettings() {
    document.getElementById('settingsModal').style.display = 'block';
    document.getElementById('settingsOverlay').style.display = 'block';
    document.getElementById('themeSelect').value = currentTheme;
    document.getElementById('languageSelect').value = currentLanguage;
}

function closeSettings() {
    document.getElementById('settingsModal').style.display = 'none';
    document.getElementById('settingsOverlay').style.display = 'none';
}

function saveSettings() {
    currentTheme = document.getElementById('themeSelect').value;
    currentLanguage = document.getElementById('languageSelect').value;
    
    localStorage.setItem('theme', currentTheme);
    localStorage.setItem('language', currentLanguage);
    
    loadTheme();
    loadLanguage();
    
    closeSettings();
}

document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    loadLanguage();
});