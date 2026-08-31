"""Run the certified Juggler descent-floor verifier.

Exact integer first-passage only. Not a halt proof.

  python tools/verify_descent_floor.py
  python tools/verify_descent_floor.py --n0 26254995
"""

from __future__ import annotations

import argparse

from research.juggler_sequence.cycle_floor_sensitivity import (
    recompute_period_bound,
    verify_floor_certified,
    write_artifacts,
    probe_payload,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n0", type=int, default=26_254_995)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()
    cert = verify_floor_certified(
        args.n0,
        workers=args.workers,
        resume=not args.no_resume,
    )
    print("verified", cert["verified"])
    print("N0", cert["N0"])
    print("max_steps", cert["max_stopping_time"], "at", cert["hardest_seed"])
    print("max_bits", cert["max_bits"], "at", cert["max_bits_seed"])
    print("total_steps", cert["total_first_passage_steps"])
    print("bit_failures", cert["bit_failures"])
    print("step_failures", cert["step_failures"])
    print("sha256", cert["sha256_chunks"])
    print("git", cert["git_commit"])
    if cert["verified"]:
        bound = recompute_period_bound(cert["N0"])
        print(bound["statement"])
        payload = probe_payload()
        payload["certificate"] = cert
        payload["period_bound"] = bound
        from research.juggler_sequence.cycle_floor_sensitivity import (
            bottleneck_note,
            classify,
        )

        payload["bottleneck"] = bottleneck_note(cert)
        payload["decision"] = classify(payload["sensitivity"], cert)
        write_artifacts(payload)


if __name__ == "__main__":
    main()
