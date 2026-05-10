# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.6.x   | :white_check_mark: |
| < 0.6   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in Eko AI Business Automation, please report it responsibly.

**Do NOT open a public GitHub issue for security bugs.**

Instead, email us directly at:

📧 **security@ekoai.com**

Please include:
- A clear description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact assessment
- Any suggested mitigation or fix

We aim to respond within **48 hours** and will keep you updated on our progress.

## Security Measures

- All secrets and API keys must be stored in `.env` (never committed to the repository)
- JWT tokens use HS256 with a minimum 32-character secret in production
- PostgreSQL password defaults are removed; fail-loud on missing credentials
- Email validation uses `EmailStr` with sanitization at discovery sources
- Rate limiting (5 contacts/day per lead) and cooldown periods enforced
- DNC registry sync runs monthly to honor opt-outs
- Sentry observability integrated (optional, loads only if `SENTRY_DSN` is set)

## Past Security Incidents

| Date | Issue | Resolution |
|------|-------|------------|
| 2026-05-09 | Live Telegram bot token exposed in AGENTS.md | Token redacted from repo; user must rotate via BotFather |
| 2026-05-09 | Real customer PII in AGENTS.md | Replaced with placeholders; user must scrub Git history |
| 2026-05-09 | Weak defaults in docker-compose.yml | Removed `eko_dev_pass` and `dev-secret-change-in-production` defaults |

---

*Last updated: 2026-05-10*
