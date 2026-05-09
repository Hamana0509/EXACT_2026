# CLAUDE.md — Operating manual

## What this is

Submission codebase for **EXACT 2026** (IJCNN / CSoNet 2026), an XAI challenge for educational QA. Two dataset families:

- **Type 1**: logic on university regulations. Released records contain `premises-NL`, `premises-FOL`, `questions`, `answers`, `explanation`. Test-set inputs give only question + NL premises.
- **Type 2**: numerical physics. Records contain `id`, `question`, `cot`, `answer`, `unit`. Test-set inputs give only the question.

The official test set is **unified** (both types interleaved). Required output fields are `answer` + `explanation`. Optional but reward-bearing: `fol`, `cot`, `premises`, `confidence`.

## Hard rules (enforced by competition)

- Open-source LLMs **≤ 8 B parameters only**. Closed-source GPT/Claude/Gemini are **forbidden** in production paths.
- Every response must include a faithful explanation. Refusing a determinable question loses points.

## Stack

FastAPI + LangChain 1.0+ + ChatOpenAI (OpenRouter, `qwen/qwen3-8b`). Pydantic v2 schemas. Structured output via `model.with_structured_output(SchemaClass, method=...)`.

## Layout (one-liner each)

- `app/main.py` — `create_app()` factory; mounts routers; global error handler.
- `app/config.py` — `pydantic-settings` loader from `.env`.
- `app/llm.py` — `build_chat_model()` returns a configured `ChatOpenAI`.
- `app/schemas/` — request + response Pydantic models per dataset type, plus shared API envelopes.
- `app/prompts/` — prompt `.md` files + `loader.load_prompt(name)`.
- `app/chains/` — `answer_type1()` / `answer_type2()`; both call `build_structured_chain()`.
- `app/routers/` — `health`, `type1`, `type2`, `unified`.
- `data/` — 3 synthetic samples per dataset type.
- `tasks/` — file-based backlog (`backlog.md`) and completion log (`done.md`).
- `tests/` — pytest smoke tests with mocked LLM.

## How to run

```bash
pip install -e ".[dev]"            # or: uv sync
cp .env.example .env               # then edit OPENAI_API_KEY
uvicorn app.main:app --reload      # API on :8000
pytest -q                          # smoke tests
```

## Conventions

- One Pydantic model per request and response. Never expose raw `dict` on the wire.
- Prompts live as `.md` in `app/prompts/`. Load via `prompts.loader.load_prompt`. Do not inline prompt strings in chain code.
- When you graduate from a one-shot chain to tool-using reasoning (calculator for physics, Z3 for logic), use **`create_agent()`** from `langchain.agents`. Do not use the legacy `AgentExecutor`.
- Pin `langchain >= 1.0`. Never downgrade to 0.3 (legacy maintenance only).
- All structured-output chains accept a `STRUCTURED_OUTPUT_METHOD` env knob. Default is `json_schema`; fall back to `function_calling` or `json_mode` if the model rejects.
- Logging uses `app.log.setup_logging()` which installs `rich.logging.RichHandler`. In modules: `from app.log import get_logger; log = get_logger(__name__)`. Call `setup_logging()` once at process startup (already done in `app/main.py` and `scripts/run_test.py`). Log level via `LOG_LEVEL` env (default `INFO`). Use Rich markup (`[cyan]...[/cyan]`, `[bold]...[/bold]`) inside log messages for inline color.

## Working with `tasks/`

- Read `tasks/backlog.md` before starting work; the order is priority order.
- When a task is complete, **move** the line (don't copy) to `tasks/done.md` with a date prefix: `- [x] YYYY-MM-DD <title> — <one-line context>`.
- Edit by hand or via Claude. No external tracker.

## Skills to invoke (langchain-skills plugin)

The plugin is installed at `~/.claude/plugins/cache/langchain-skills/`. Before writing chain or agent code, invoke:

- `langchain-fundamentals` — `create_agent`, tools, structured output, middleware.
- `langchain-dependencies` — version pinning reference.
- `framework-selection` — LangChain vs LangGraph vs Deep Agents (revisit when reasoning grows multi-step).
- `langchain-rag` — when adding few-shot retrieval over the organizer dataset.
