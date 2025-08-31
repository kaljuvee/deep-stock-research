import argparse
import logging
import os
from pathlib import Path
from datetime import datetime
import re
import sys
from typing import List

# Ensure imports resolve when running from project root
try:
    from research_agent import run_stock_research
except Exception as import_error:
    logging.exception("Failed to import run_stock_research from research_agent")
    raise


DEFAULT_QUERIES: List[str] = [
    "Give me a quick overview and current price for AAPL.",
    "Provide key financial statement metrics for MSFT.",
    "Analyze recent trend and indicators for NVDA.",
]


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Deep Stock Research Agent from the command line"
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="Research question(s) to run. If none provided, runs default queries.",
    )
    parser.add_argument(
        "--out-dir",
        default="data",
        help="Directory to write outputs (default: data)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args(argv)


def _sanitize_for_filename(text: str, fallback: str) -> str:
    """Create a safe filename component from arbitrary text."""
    if not text:
        return fallback
    # Lowercase, replace non-alphanum with hyphens, collapse repeats, trim
    safe = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return safe or fallback


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    queries = args.query if args.query else DEFAULT_QUERIES

    # Ensure output directory exists
    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, q in enumerate(queries, start=1):
        print("\n" + "=" * 80)
        print(f"Query {idx}/{len(queries)}: {q}")
        print("-" * 80)
        try:
            result = run_stock_research(q)
        except Exception as e:
            logging.exception("Error running research query")
            print(f"Error: {e}")
            continue

        output_text = result if isinstance(result, str) else str(result)
        print(output_text)

        # Write output to file
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        base = _sanitize_for_filename(q[:80], f"query-{idx}")
        filename = f"{timestamp}-{base}.txt"
        out_path = output_dir / filename
        try:
            with out_path.open("w", encoding="utf-8") as f:
                f.write(output_text)
            print(f"Saved output: {out_path}")
        except Exception as write_err:
            logging.exception("Failed to write output file")
            print(f"Error saving output to {out_path}: {write_err}")
        print("=" * 80 + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


