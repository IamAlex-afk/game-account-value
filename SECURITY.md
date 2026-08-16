# Security Policy

## Supported Versions

Only the latest version deployed at
https://iamalex-afk.github.io/game-account-value/ is supported.

## Architecture

This is a browser-only static landing page on GitHub Pages.

- No server — no backend to attack
- No database — no data to steal
- No user accounts — no credentials to compromise
- No forms, no data collection (form-action 'none' in CSP)
- Content Security Policy active
- All interaction happens via a link out to the Telegram bot
  (@GameAccountValue_Bot), which is a separate service with its own
  security policy

## Reporting a Vulnerability

Report security issues via GitHub Issues:
https://github.com/IamAlex-afk/game-account-value/issues

Expected response time: within 7 days.
