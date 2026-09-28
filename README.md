# Copilot Studio AI Agent Reliability & Data Quality Lab

Portfolio project focused on Microsoft Copilot Studio, agent evaluation, tool use, data quality, and documentation quality.

## What this project demonstrates

- Microsoft Copilot Studio agent design
- Grounded IT-support knowledge
- REST/OpenAPI tools backed by FastAPI
- Customer/device lookup and synthetic ticket creation
- Data-quality validation and normalization
- Stale/conflicting documentation testing
- Agent evaluation cases and failure analysis
- pytest regression tests
- uv-based Python workflow

## Architecture

```text
Copilot Studio Agent
    ├── Website / knowledge sources
    ├── REST/OpenAPI tools
    │      └── FastAPI
    │            ├── customer lookup
    │            ├── device lookup
    │            └── ticket creation
    └── Evaluation cases

Python data-quality pipeline
    ├── missing values
    ├── invalid formats
    ├── normalization
    └── duplicates
```

## Local setup with uv

```powershell
uv python install 3.12
uv python pin 3.12
uv sync
uv run python -m data_quality.run_checks
uv run python -m pytest -q
uv run uvicorn api.main:app --reload --port 8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Copilot Studio

See:

- `copilot_studio/AGENT_INSTRUCTIONS.txt`
- `docs/COPILOT_STUDIO_SETUP.md`
- `evals/agent_eval_cases.json`

## Knowledge website

The `docs/` folder also contains simple HTML pages designed for GitHub Pages so Copilot can use them as website knowledge sources.

All data are synthetic. No PHI, PII, real credentials, or production secrets are included.
