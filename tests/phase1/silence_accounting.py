"""Per-cohort silence accounting: WHY each silent cohort is silent.

PREREG.md §39: a silence is honest only with its domain attached. A merged
result gives `evidence_outcome` per COMBINATION, which is the wrong grain for
this question -- a combination reads `finding` if any cohort produced one, so a
cohort that produced nothing is invisible in it.

THE DISTINCTION THIS EXISTS TO PRESERVE, from §6.6's own table:

    observed_silence   at least one valid execution occurred and none produced
                       a finding                     -> the probe HAPPENED and
                                                        found nothing
    none               no valid execution occurred   -> the probe DID NOT HAPPEN

**A probe that did not happen found nothing, and that is not the same as a probe
that happened and found nothing.** B8.3 separated `trades.action` and
`trades.symbol` from the other twelve silences on exactly this ground. Collapsing
them would report a coverage hole as evidence of cleanliness, which is the error
this whole tool exists to catch other tools making.

So each silent cohort is reported with the strategies that ran VALIDLY, the ones
that did not, and the recorded reason for each failure -- never a bare "silent".

    usage: silence_accounting.py <merged.json> [detector-id ...]
"""
from __future__ import annotations

import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:                                       # noqa: BLE001
    pass

MERGED = pathlib.Path(sys.argv[1])
WANTED = sys.argv[2:]
d = json.loads(MERGED.read_text(encoding="utf-8"))


def blocks(doc):
    """Yield (detector_id, records, dependency_map, silent) for each detector."""
    if "detectors" in doc and isinstance(doc["detectors"], dict):
        for det, b in doc["detectors"].items():
            yield det, b.get("_records"), b.get("dependency_map", {}), \
                b.get("silent_cohorts", [])
    else:                                            # B8's single-detector shape
        yield doc.get("detector", "?"), None, doc.get("dependency_map", {}), \
            doc.get("silent_cohorts", [])


print("=" * 78)
print("SILENCE ACCOUNTING -- §39: a silence carries the domain that produced it")
print("=" * 78)
print("  merged result : %s" % MERGED.name)
print("  case          : %s" % d.get("case", "?"))
print("  cohorts       : %s" % d.get("cohorts", "?"))

# Records are needed at cohort grain. The B9 merge keeps counts per trace, so
# the per-record detail is re-read from the shards it was built from.
SHARD_DIR = pathlib.Path(d.get("_shard_dir", "")) if d.get("_shard_dir") else None
records: dict[str, list[dict]] = {}
if SHARD_DIR is None:
    import os
    SHARD_DIR = pathlib.Path(os.environ.get(
        "LEAKAUDIT_B9_SHARD_DIR", str(pathlib.Path.home() / ".leakaudit_b9")))
shards = sorted(SHARD_DIR.glob("b9_shard_*_of_*.json"))
if not shards:
    sys.exit("HALT: no shard files under %s. This accounting needs per-record "
             "detail, which the merged file summarises away -- and reporting "
             "silence without it is the thing §39 forbids." % SHARD_DIR)
for p in shards:
    s = json.loads(p.read_text(encoding="utf-8"))
    for det in s.get("detectors", []):
        records.setdefault(det["detector"], []).extend(det["records"])
print("  shards read   : %d, from %s" % (len(shards), SHARD_DIR))
print()

for det, _unused, depmap, silent in blocks(d):
    if WANTED and det not in WANTED:
        continue
    recs = records.get(det, [])
    print("=" * 78)
    print("%s -- %d fired, %d silent" % (det, len(depmap), len(silent)))
    print("=" * 78)
    if not recs:
        print("  no records for this detector in the shards; nothing to account for")
        continue
    by_cohort: dict[str, list[dict]] = {}
    for r in recs:
        by_cohort.setdefault(r["cohort"], []).append(r)

    print("  %-30s %-26s %s" % ("cohort", "ran VALIDLY", "invalid, and why"))
    outcomes = {"observed_silence": [], "none": []}
    for cid in sorted(silent):
        rs = by_cohort.get(cid, [])
        valid = sorted({r["strategy"] for r in rs if r["valid"]})
        invalid = sorted({"%s=%s" % (r["strategy"], r["failure_reason"])
                          for r in rs if not r["valid"]})
        # §6.6: `none` iff NO valid execution occurred.
        outcome = "observed_silence" if valid else "none"
        outcomes[outcome].append(cid)
        print("  %-30s %-26s %s"
              % (cid, ", ".join(valid) if valid else "**NONE**",
                 ", ".join(invalid) if invalid else "—"))

    print()
    print("  observed_silence : %d  -- the probe HAPPENED and found nothing"
          % len(outcomes["observed_silence"]))
    print("  none             : %d  -- NO valid execution; the probe did not happen"
          % len(outcomes["none"]))
    if outcomes["none"]:
        print("      %s" % ", ".join(outcomes["none"]))
        print("      Reporting these as silence would claim a probe that never ran.")
    print()
