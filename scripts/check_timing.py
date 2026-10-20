#!/usr/bin/env python3
"""Check a constant-dt MD stage's declared duration; never run a simulation.

Exit 0: arithmetic agrees. Exit 1: declared duration disagrees.
Exit 2: invalid input. This does not validate physics, sampling or approval.
"""

import argparse
import json
from decimal import Decimal, InvalidOperation, localcontext


def positive_decimal(value):
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError("must be a finite positive number") from exc
    if not parsed.is_finite() or parsed <= 0:
        raise argparse.ArgumentTypeError("must be a finite positive number")
    return parsed


def positive_integer(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dt-fs", type=positive_decimal, required=True)
    parser.add_argument("--steps", type=positive_integer, required=True)
    parser.add_argument("--expected-ns", type=positive_decimal, required=True)
    parser.add_argument(
        "--interval-steps", type=positive_integer, action="append", default=[],
        help="Repeat for each reporter. Counts assume this stage starts at step 0.",
    )
    args = parser.parse_args()
    with localcontext() as ctx:
        ctx.prec = max(28, len(args.dt_fs.as_tuple().digits) + len(str(args.steps)) + 16)
        duration = Decimal(args.steps) * args.dt_fs / Decimal(1000000)
        intervals = []
        for interval in args.interval_steps:
            count, remainder = divmod(args.steps, interval)
            intervals.append({
                "interval_steps": interval,
                "interval_ns": str(Decimal(interval) * args.dt_fs / Decimal(1000000)),
                "periodic_outputs_excluding_initial_and_extra_final": count,
                "steps_after_last_periodic_output": remainder,
                "warning": "no periodic output within this stage" if count == 0 else None,
            })
        agrees = duration == args.expected_ns
        print(json.dumps({
            "dt_fs": str(args.dt_fs),
            "steps": args.steps,
            "computed_duration_ns": str(duration),
            "declared_duration_ns": str(args.expected_ns),
            "timing_matches": agrees,
            "intervals": intervals,
            "scope": "Arithmetic only; physics, convergence and authorization are not assessed.",
        }, indent=2))
    return 0 if agrees else 1


if __name__ == "__main__":
    raise SystemExit(main())
