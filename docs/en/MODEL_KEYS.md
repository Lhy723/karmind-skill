# Model API Key Configuration

`karmind-skill` model batch ingest uses an OpenAI-compatible `/chat/completions` API. You can use OpenAI, an OpenAI-compatible gateway, or a self-hosted compatible service.

## Recommended Setup

Prefer environment variables. Do not write real API keys into wiki pages, source notes, logs, or reports.

macOS / Linux:

```bash
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="model-name"
export LLM_API_KEY="sk-..."
```

Windows PowerShell:

```powershell
$env:LLM_BASE_URL = "https://api.openai.com/v1"
$env:LLM_MODEL = "model-name"
$env:LLM_API_KEY = "sk-..."
```

Then run from the wiki project directory:

macOS / Linux:

```bash
python /tmp/karmind-skill/scripts/model_batch_ingest.py . --dry-run
python /tmp/karmind-skill/scripts/model_batch_ingest.py . --limit 10
```

Windows PowerShell:

```powershell
python "$env:TEMP\karmind-skill\scripts\model_batch_ingest.py" . --dry-run
python "$env:TEMP\karmind-skill\scripts\model_batch_ingest.py" . --limit 10
```

This assumes you cloned this repository to `/tmp/karmind-skill` or `$env:TEMP\karmind-skill` on Windows. If you use another location, replace the path accordingly.

Default output is review drafts:

```text
wiki/sources/_drafts/
```

The cache status becomes `drafted`, not `processed`. Promote reviewed notes into `wiki/sources/` afterward.

## Local `.env.local`

If you do not want to export variables every time, create `.env.local` in the wiki project root:

```bash
cp .env.example .env.local
```

If the current wiki project does not contain `.env.example`, create `.env.local` directly with the fields below.

Fill in:

```dotenv
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=model-name
LLM_API_KEY=sk-...
```

`.gitignore` excludes `.env` and `.env.*`, while keeping `.env.example`. Do not commit `.env.local`.

## Compatible Variable Names

The script reads:

- `LLM_API_KEY`, with `OPENAI_API_KEY` fallback
- `LLM_MODEL`, with `OPENAI_MODEL` fallback
- `LLM_BASE_URL`, with `OPENAI_BASE_URL` fallback

CLI flags `--api-key`, `--model`, and `--base-url` can override environment variables, but avoid putting keys into shell history.

## Security Advice

- Create a separate API key for wiki batch processing.
- Set usage limits and revocable permissions.
- Do not write keys into `AGENTS.md`, `wiki/log.md`, `wiki/reports/`, or source notes.
- If a key leaks, revoke it immediately in the provider dashboard.
