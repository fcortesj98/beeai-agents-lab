"""Command-line interface.

    python3.11 -m beeai_lab list
    python3.11 -m beeai_lab check-env
    python3.11 -m beeai_lab run 05
    python3.11 -m beeai_lab run react-agent --query "Assess ransomware risk for hospitals"
    python3.11 -m beeai_lab run 05 06 07          # compare capability levels
    python3.11 -m beeai_lab run all
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from collections.abc import Sequence

from beeai_lab import __version__
from beeai_lab.config import configure_environment
from beeai_lab.examples import EXAMPLES, Example, ExampleOptions, get_example
from beeai_lab.examples.environment import print_environment_report
from beeai_lab.utils import console
from beeai_lab.utils.errors import hint_for, root_cause
from beeai_lab.utils.runtime import enable_debug_if_requested, quiet_logging


def _print_list() -> None:
    print(f"{'ID':<4}{'NAME':<20}{'LAB FILE':<10}CONCEPT")
    for ex in EXAMPLES:
        flag = "  [asks for approval]" if ex.interactive else ""
        print(f"{ex.id:<4}{ex.slug:<20}{ex.original_script:<10}{ex.concept}{flag}")


def _resolve(targets: Sequence[str]) -> list[Example]:
    if [t.lower() for t in targets] == ["all"]:
        return [ex for ex in EXAMPLES if ex.id != "01"]
    return [get_example(t) for t in targets]


async def _run_examples(examples: Sequence[Example], options: ExampleOptions) -> int:
    for ex in examples:
        console.banner(f"{ex.id} · {ex.title} — {ex.concept}  (lab: {ex.original_script})")
        try:
            await ex.run(options)
        except KeyboardInterrupt:
            print("\nInterrupted.")
            return 130
        except Exception as exc:  # report and stop, with a hint when we recognize the failure
            print(f"\n❌ {ex.slug} failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            cause = root_cause(exc)
            if cause is not exc:
                first_line = (str(cause).strip().splitlines() or [""])[0][:300]
                print(f"   Root cause: {type(cause).__name__}: {first_line}", file=sys.stderr)
            hint = hint_for(exc)
            if hint:
                print(f"\n💡 {hint}", file=sys.stderr)
            else:
                print("\nRe-run with BEEAI_DEBUG=1 for the provider's raw error.", file=sys.stderr)
            return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="beeai_lab",
        description="Run the BeeAI Framework lab examples, from a single chat call to a multi-agent system.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all examples")
    sub.add_parser("check-env", help="Show configured models and which credentials are set")

    run = sub.add_parser("run", help="Run one or more examples")
    run.add_argument("targets", nargs="+", help='Example number, name or lab file (e.g. 5, react-agent, t12), or "all"')
    run.add_argument("-q", "--query", help="Replace the example's default user input")
    run.add_argument("-m", "--model", help='Override the model, e.g. "openai:gpt-4o-mini"')
    run.add_argument(
        "--no-approval",
        action="store_true",
        help="Skip human-in-the-loop approval prompts in example 12 (travel planner)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "list":
        _print_list()
        return 0

    configure_environment()
    if args.command == "check-env":
        return 0 if print_environment_report() else 1

    quiet_logging()
    enable_debug_if_requested()
    try:
        examples = _resolve(args.targets)
    except KeyError as exc:
        print(exc.args[0], file=sys.stderr)
        return 2

    options = ExampleOptions(query=args.query, model=args.model, require_approval=not args.no_approval)
    return asyncio.run(_run_examples(examples, options))


if __name__ == "__main__":
    raise SystemExit(main())
