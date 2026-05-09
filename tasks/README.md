# tasks/

A lightweight, version-controlled task tracker. No external service.

## Files

- `backlog.md` — open work, in **priority order** (top = next). Sectioned by horizon: Now / Soon / Later.
- `done.md` — completed work, newest at top.

## Format

Open task:
```
- [ ] Short title — one-line context (optional)
```

Completed task — **move** the line to `done.md` with a date prefix:
```
- [x] YYYY-MM-DD Short title — one-line context
```

## Etiquette

- Don't duplicate tasks. If something needs to grow, edit the existing line.
- Re-rank `backlog.md` whenever priorities change.
- Move (not copy) finished items into `done.md` so `backlog.md` stays small.
- Keep titles short. Put rationale in a one-line context, or in the related PR/commit.
