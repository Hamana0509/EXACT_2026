# Done

- [x] 2026-05-08 Project scaffold — pyproject, .env.example, CLAUDE.md, README, tasks/ tree
- [x] 2026-05-08 Pydantic schemas for Type 1 & Type 2 — match organizer field names (`premises-NL`, `premises-FOL`, etc.)
- [x] 2026-05-08 Prompt files — `system_base`, `type1_logic`, `type2_physics` in `app/prompts/`
- [x] 2026-05-08 LangChain chains with `with_structured_output()` — pluggable method via env (`json_schema` default)
- [x] 2026-05-08 FastAPI endpoints — `/health`, `/api/v1/type1/answer`, `/api/v1/type2/answer`, `/api/v1/answer` (unified dispatcher)
- [x] 2026-05-08 Synthetic data — 3 samples per type in `data/`, covering MCQ / Yes-No-Uncertain / open (Type 1) and parallel R / capacitor energy / Kirchhoff (Type 2)
- [x] 2026-05-08 Smoke tests — `pytest` with mocked LLM, exercises all four endpoints
- [x] 2026-05-08 Batch runner — `scripts/run_test.py` reads a JSON file of records (auto-detects Type 1 vs Type 2 per record), runs each through the chain, writes a timestamped result file to `test_result/` with per-record latency + error info and a run summary
- [x] 2026-05-08 Tightened API schemas — `Type1Question`/`Type2Question` now mirror evaluation inputs strictly (no FOL/question_type/id). Added `Type1Record`/`Type2Record` for dataset loading with `.to_question()` extractors used by `scripts/run_test.py`
- [x] 2026-05-08 Colored logging — `app/log.py` with `RichHandler` (idempotent `setup_logging`, `LOG_LEVEL` env knob). Wired into `app/main.py`, `app/chains/{base,type1,type2}.py`, and `scripts/run_test.py`. Noisy third-party loggers (httpx/openai/urllib3) muted to WARNING.
- [x] 2026-05-08 Rich response logging — `log_answer()` in `app/log.py` pretty-prints the full structured response (answer, confidence, explanation, cot steps, fol formulas, premises). Each section gets a colored heading; premise sources (given/derived/external) are color-coded. Called from both Type 1 and Type 2 chains after a successful invoke.
