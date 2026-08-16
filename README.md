# GameAccountValue — лендинг (GitHub Pages)

Лендинг-страница, ведёт трафик в Telegram-бота GameAccountValue.
Отдельная папка, отдельный деплой (GitHub Pages). Не связан с `GAV_WORLDCLASS` и `GAV_MINIAPP`.

**Сайт:** https://iamalex-afk.github.io/game-account-value/

## Структура

- `index.html` — главная страница (английский)
- `{lang}/index.html` — локализации: ru, es, pt, id, tr, ar, vi, hi, fr, de, it, ja, ko, th
- `privacy.html`, `terms.html` — юридические страницы
- `robots.txt`, `sitemap.xml` — SEO
- `llms.txt`, `schema_org.json` — структурированные данные для поисковиков и AI-краулеров
- `manifest.json`, `favicon.svg`/`favicon.png`, `og-image.png` — PWA и соцсети
- `.well-known/security.txt` — контакт для security-репортов

## Деплой

Автодеплой на GitHub Pages при пуше в `main`.
