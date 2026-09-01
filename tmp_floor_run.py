import json

from research.juggler_sequence.cycle_floor_sensitivity import (
    verify_floor_certified,
)


def main() -> None:
    cert = verify_floor_certified(162_849_448, n_from=26_254_996, workers=4)
    print(json.dumps({k: cert[k] for k in (
        "N0", "n_from", "verified", "odds_walked", "max_stopping_time",
        "hardest_seed", "max_bits", "step_failures", "bit_failures",
        "other_failures",
    )}, indent=1))


if __name__ == "__main__":
    main()
