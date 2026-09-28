# Security

- Never commit `.env`, Gmail app passwords, API keys, CVs, certificates, or other personal credentials.
- Keep `SEND_REAL_EMAILS=False` while testing.
- Real sending additionally requires `ALLOW_REAL_EMAILS=True` as an explicit safety switch.
- Review generated recipients and application text before enabling real sending.
- Rotate any credential that has ever been committed to Git history.
