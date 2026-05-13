// Настройки темы и языка
let currentTranslations = {};

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const themeLink = document.getElementById('theme-style');
    if (themeLink) {
        themeLink.href = `/static/css/themes/${savedTheme}.css`;
    }
}

function loadLanguage() {
    const savedLanguage = localStorage.getItem('language') || 'ru';
    fetch(`/static/i18n/${savedLanguage}.json`)
        .then(response => response.json())
        .then(translations => {
            currentTranslations = translations;
            updateAllTranslations();
            document.title = translations.app_name || 'Weyrix';
        })
        .catch(err => console.error('Language load error:', err));
}

function updateAllTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (currentTranslations[key]) {
            // Сохраняем эмодзи, если они есть
            const emojiMatch = el.innerHTML.match(/^[🔒👥💬⭐📎📝🗑️🚪➕👤❌←\s]+/);
            const emoji = emojiMatch ? emojiMatch[0] : '';
            
            if (el.tagName === 'INPUT' && el.placeholder) {
                el.placeholder = currentTranslations[key];
            } else if (el.tagName === 'BUTTON') {
                if (emoji) {
                    el.innerHTML = `${emoji} ${currentTranslations[key]}`;
                } else {
                    el.textContent = currentTranslations[key];
                }
            } else {
                el.textContent = currentTranslations[key];
            }
        }
    });
}

function openSettings() {
    document.getElementById('settingsModal').style.display = 'block';
    document.getElementById('settingsOverlay').style.display = 'block';
    document.getElementById('themeSelect').value = localStorage.getItem('theme') || 'dark';
    document.getElementById('languageSelect').value = localStorage.getItem('language') || 'ru';
}

function closeSettings() {
    document.getElementById('settingsModal').style.display = 'none';
    document.getElementById('settingsOverlay').style.display = 'none';
}

function saveSettings() {
    const theme = document.getElementById('themeSelect').value;
    const language = document.getElementById('languageSelect').value;
    localStorage.setItem('theme', theme);
    localStorage.setItem('language', language);
    loadTheme();
    loadLanguage();
    closeSettings();
}

// Загружаем при старте
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    loadLanguage();
});

// Экспортируем функцию для использования в других страницах
window.updateTranslations = updateAllTranslations;