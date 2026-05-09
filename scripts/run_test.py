"""Batch-run dataset records through the chains and save results to test_result/.

Reads a JSON file (a list of records), runs each one through the appropriate
chain (`answer_type1` or `answer_type2`), and writes a single combined result
file to the output directory.

Usage:
    uv run python scripts/run_test.py data/dataset_type1_sample.json
    uv run python scripts/run_test.py data/dataset_type2_sample.json --type type2
    uv run python scripts/run_test.py path/to/test.json --limit 5

Type detection ('--type auto', the default) looks for `premises-NL` in each
record — present means Type 1, absent means Type 2. This mirrors the official
unified test-set format.

Output:
    test_result/<YYYYMMDD-HHMMSS>_<input_stem>.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

# Allow running this file directly: `uv run python scripts/run_test.py ...`
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.chains.type1 import answer_type1  # noqa: E402
from app.chains.type2 import answer_type2  # noqa: E402
from app.log import get_logger, setup_logging  # noqa: E402
from app.schemas.type1 import Type1Question, Type1Record  # noqa: E402
from app.schemas.type2 import Type2Question, Type2Record  # noqa: E402

setup_logging()
log = get_logger("scripts.run_test")


DatasetType = str  # "type1" | "type2"


def detect_dataset_type(record: dict) -> DatasetType:
    """Return 'type1' if the record carries NL premises, else 'type2'."""
    nl = record.get("premises-NL") or record.get("premises_nl")
    return "type1" if nl else "type2"


def build_type1_request(record: dict) -> Type1Question:
    """Build a Type1Question (strict evaluation input) from a dataset record.

    Dataset records may carry FOL / answers / explanation; those are dropped.
    Records with `questions` as a list use the first entry. Records with a
    scalar `question` are also accepted (e.g. our run_test fixtures).
    """
    if "questions" in record or "premises-FOL" in record or "answers" in record:
        # Looks like a full dataset record — validate via Type1Record then extract.
        return Type1Record.model_validate(record).to_question()

    return Type1Question.model_validate(
        {
            "premises-NL": record.get("premises-NL", record.get("premises_nl", [])),
            "question": record["question"],
        }
    )


def build_type2_request(record: dict) -> Type2Question:
    """Build a Type2Question (strict evaluation input) from a dataset record.

    Dataset records carry `id` / `cot` / `answer` / `unit`; those are dropped.
    Record `id` is preserved in the result's `input` block for downstream
    submission scripts.
    """
    if {"id", "cot", "answer", "unit"} & record.keys():
        return Type2Record.model_validate(record).to_question()
    return Type2Question(question=record["question"])


def run_record(record: dict, dataset_type: DatasetType) -> dict:
    """Run one record. Catches any exception and returns it in the result."""
    start = time.perf_counter()
    try:
        if dataset_type == "type1":
            ans = answer_type1(build_type1_request(record))
        else:
            ans = answer_type2(build_type2_request(record))
        return {
            "input": record,
            "output": ans.model_dump(),
            "error": None,
            "latency_ms": int((time.perf_counter() - start) * 1000),
        }
    except Exception as e:
        return {
            "input": record,
            "output": None,
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc(),
            },
            "latency_ms": int((time.perf_counter() - start) * 1000),
        }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("input", type=Path, help="Path to the input JSON file (a list of records).")
    parser.add_argument(
        "--type",
        choices=["type1", "type2", "auto"],
        default="auto",
        help="Dataset type. 'auto' detects per-record by presence of `premises-NL`.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "test_result",
        help="Directory for the result JSON (default: test_result/).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="If given, only run the first N records.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    raw = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        log.error("expected a JSON array of records, got %s", type(raw).__name__)
        return 2
    records = raw[: args.limit] if args.limit else raw

    args.output_dir.mkdir(parents=True, exist_ok=True)
    log.info("[bold]Loaded %d record(s)[/bold] from %s", len(records), args.input)

    results: list[dict] = []
    n_success = n_error = 0
    total_latency = 0

    for i, record in enumerate(records):
        dataset_type = args.type if args.type != "auto" else detect_dataset_type(record)
        log.info("[bold]>>> [%d/%d] type=%s[/bold]", i + 1, len(records), dataset_type)
        result = run_record(record, dataset_type)
        result["dataset_type"] = dataset_type
        result["index"] = i
        results.append(result)

        total_latency += result["latency_ms"]
        if result["error"] is None:
            n_success += 1
        else:
            n_error += 1
            log.error(
                "[red]record %d failed[/red]: %s: %s",
                i,
                result["error"]["type"],
                result["error"]["message"],
            )

    summary = {
        "input_file": str(args.input),
        "ran_at": datetime.now().isoformat(timespec="seconds"),
        "n_total": len(records),
        "n_success": n_success,
        "n_error": n_error,
        "avg_latency_ms": int(total_latency / len(records)) if records else 0,
    }

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = args.output_dir / f"{timestamp}_{args.input.stem}.json"
    out_path.write_text(
        json.dumps({"summary": summary, "results": results}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    color = "green" if n_error == 0 else "yellow"
    log.info(
        "[bold %s]=== Summary ===[/bold %s] total=%d success=%d error=%d avg_latency=%d ms",
        color,
        color,
        summary["n_total"],
        summary["n_success"],
        summary["n_error"],
        summary["avg_latency_ms"],
    )
    log.info("[dim]wrote[/dim] %s", out_path)
    return 0 if n_error == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
