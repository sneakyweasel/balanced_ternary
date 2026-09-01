import json

from research.juggler_sequence.cycle_walk_charge import certified_report

r = certified_report(176_251, 162_849_448)
print(json.dumps(r, indent=1))
