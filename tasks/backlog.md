# Backlog

Listed top-down in priority order within each section.

## Now (next 1–2 sessions)

- [ ] Wait for organizer dataset (May 4–9) and write `scripts/load_organizer_data.py` to map their JSON into `Type1Question` / `Type2Question`
- [ ] `scripts/eval_p1.py` — answer-correctness on held-out organizer data; CSV/JSON report
- [ ] Few-shot prompts — store 3–5 worked examples per type and inject via the prompt loader
- [ ] Submission packaging script — produce organizer-format JSON output for the test set

## Soon

- [ ] LangFuse callbacks — wire `CallbackHandler` into `chains/base.py`; trace every LLM call
- [ ] Self-consistency / majority-vote sampling for hard Type 2 problems (n=5, vote on numeric answer)
- [ ] Calculator tool for Type 2 — graduate to `create_agent()` with a Python eval tool
- [ ] Prompt iteration on `type1_logic.md` / `type2_physics.md` after looking at first eval failures

## Later

- [ ] Z3 / FOL verification step for Type 1 — chain calls solver after LLM emits `fol`; flag inconsistencies
- [ ] RAG over university-regulations corpus for Type 1 (use the `langchain-rag` skill)
- [ ] Dockerfile + healthcheck for reproducible submission
- [ ] Confidence calibration — log confidence vs. correctness, fit a temperature
