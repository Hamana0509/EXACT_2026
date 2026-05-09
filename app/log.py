"""Project-wide logging configuration.

Uses `rich.logging.RichHandler` for colored output. Call `setup_logging()`
once at process startup (FastAPI app factory, script entrypoints); subsequent
`logging.getLogger(name)` calls inherit the formatting.

Color comes from the level name (DEBUG=cyan, INFO=blue, WARNING=yellow,
ERROR=red, CRITICAL=red bg). Tracebacks render with syntax highlighting.

Configuration:
    LOG_LEVEL env var (default INFO). Accepts standard logging level names.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from pydantic import BaseModel
from rich.logging import RichHandler

_CONFIGURED = False

_NOISY_LOGGERS = (
    "httpx",
    "httpcore",
    "openai",
    "openai._base_client",
    "urllib3",
    "asyncio",
)


def setup_logging(level: str | int | None = None) -> None:
    """Install RichHandler as the root logging handler. Idempotent."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    resolved = level if level is not None else os.getenv("LOG_LEVEL", "INFO")

    handler = RichHandler(
        level=resolved,
        rich_tracebacks=True,
        tracebacks_show_locals=False,
        show_path=False,
        markup=True,
        log_time_format="[%H:%M:%S]",
    )

    logging.basicConfig(
        level=resolved,
        format="%(name)s | %(message)s",
        datefmt="[%X]",
        handlers=[handler],
        force=True,
    )

    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Convenience wrapper around `logging.getLogger`."""
    return logging.getLogger(name)


def log_answer(log: logging.Logger, label: str, answer: BaseModel) -> None:
    """Pretty-print a structured chain response with Rich markup.

    Renders `answer`, `unit`, `confidence`, `explanation`, and the optional
    `cot` / `fol` / `premises` blocks as a single multi-line INFO log entry.
    Fields that are `None` are omitted.
    """
    data: dict[str, Any] = answer.model_dump(exclude_none=True)
    lines: list[str] = [f"[bold green]{label}[/bold green] response:"]

    for key in ("answer", "unit", "confidence"):
        if key in data:
            lines.append(f"  [bold]{key}[/bold]: {data[key]!r}")

    if "explanation" in data:
        lines.append(f"  [bold]explanation[/bold]: {data['explanation']}")

    cot = data.get("cot")
    if cot:
        lines.append(f"  [bold cyan]cot[/bold cyan] ({len(cot)} step(s)):")
        for s in cot:
            lines.append(f"    [dim]{s['step']}.[/dim] {s['reasoning']}")

    fol = data.get("fol")
    if fol:
        lines.append(f"  [bold yellow]fol[/bold yellow] ({len(fol)} formula(s)):")
        for f in fol:
            desc = f"  [dim]-- {f['description']}[/dim]" if f.get("description") else ""
            lines.append(f"    [yellow]{f['formula']}[/yellow]{desc}")

    premises = data.get("premises")
    if premises:
        lines.append(f"  [bold magenta]premises[/bold magenta] ({len(premises)}):")
        for p in premises:
            src = p.get("source", "given")
            src_color = {"given": "green", "derived": "cyan", "external": "blue"}.get(src, "white")
            lines.append(
                f"    [cyan]\\[{p['id']}][/cyan] [{src_color}]({src})[/{src_color}] {p['statement']}"
            )

    log.info("\n".join(lines))
