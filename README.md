# EXACT 2026 — XAI Educational QA

Submission codebase for [EXACT 2026](https://ura.hcmut.edu.vn/exact), the IJCNN/CSoNet 2026 challenge for transparent educational question-answering.

## Stack

- **FastAPI** — HTTP API surface
- **LangChain 1.0+** — `with_structured_output()` for typed responses
- **ChatOpenAI** via OpenRouter — model `qwen/qwen3-8b` (≤ 8B open-source, per competition rules)
- **Pydantic v2** — request/response schemas

## Quick start

```bash
# 1. Install
pip install -e ".[dev]"        # or: uv sync

# 2. Configure
cp .env.example .env
# edit .env with your OpenRouter API key

# 3. Run the API
uvicorn app.main:app --reload

# 4. Smoke test
pytest -q
curl http://localhost:8000/health
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness + configured model name |
| `POST` | `/api/v1/type1/answer` | Logic question (with NL premises) |
| `POST` | `/api/v1/type2/answer` | Physics question (numerical) |
| `POST` | `/api/v1/answer` | Unified dispatcher (matches official test set) |

Interactive docs: <http://localhost:8000/docs>

## Batch evaluation

Run a JSON file of records through the chains and save results to `test_result/`:

```bash
uv run python scripts/run_test.py data/dataset_type1_sample.json
uv run python scripts/run_test.py path/to/test.json --limit 10
```

The script auto-detects Type 1 vs Type 2 per record (presence of `premises-NL`), so it works on the official unified test set. Output: `test_result/<timestamp>_<input_stem>.json` with per-record latency, error info, and a run summary.

## Layout

```
app/
  main.py          FastAPI app factory
  config.py        Settings (.env loader)
  llm.py           ChatOpenAI factory
  schemas/         Pydantic request/response models
  prompts/         Markdown prompt templates + loader
  chains/          LangChain chains (one per dataset type)
  routers/         FastAPI routers
data/              Synthetic samples (3 per type)
tasks/             Backlog + done log (file-based tracker)
tests/             pytest smoke tests
```

See [`CLAUDE.md`](./CLAUDE.md) for the full operating manual.
