# Copilot Studio Setup

## 1. Create the agent

Name:

IT Support Quality Lab

Paste the contents of:

copilot_studio/AGENT_INSTRUCTIONS.txt

into the agent instructions.

## 2. Add website knowledge

Because some Microsoft 365 Copilot environments restrict direct file/SharePoint knowledge, this repo includes HTML pages in docs/ for GitHub Pages.

After enabling GitHub Pages from the main branch and /docs folder, add the public site URL as website knowledge.

## 3. Run the backend

```powershell
uv sync
uv run python -m data_quality.run_checks
uv run uvicorn api.main:app --reload --port 8000
```

Open:

http://127.0.0.1:8000/docs

## 4. Tool integration

After deploying the FastAPI service to a public HTTPS endpoint, use:

https://YOUR-HOST/openapi.json

for the REST/OpenAPI tool definition.

## 5. Baseline evaluation

Run the cases in:

evals/agent_eval_cases.json

Record pass/fail, returned answer, source/tool used, and failure category.

## 6. Stale-document experiment

After the baseline is working, introduce the archived VPN policy and test whether the agent continues to prefer the current 2026 policy.
