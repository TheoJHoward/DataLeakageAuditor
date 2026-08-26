#!/usr/bin/env python3
"""DELTA R67 / §16.3 - the negative test, as a mutation battery.

§16.3 asks for ONE deliberately wrong literal. One mutation tests one assertion;
this detector makes six (D1, D2, D2-order, D3, D4, and the drift/authority guards),
and H-L16 says a check is mutation-tested against its own design's admitted failure
modes, not just against one example. So: one mutation per assertion, each in a
scratch copy, each expected to FIRE.
"""
import re, shutil, subprocess, sys, pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "33e8c843-30fa-4bfb-aa9f-814c77bdb2e6/scratchpad/mut")
NEEDED = ["AVAILABILITY_DECLARATION.md", "PREREG.md", "DESIGN.md", "HISTORY.md",
          "README.md", "evidence/ceremony/CEREMONY_COMMANDS.md",
          "evidence/ceremony/COMMIT_PLAN.md", "evidence/ceremony/DEVIATIONS_DRAFT.md",
          "evidence/ceremony/H34_DRAFT.md"]


def fresh():
    if SCR.exists():
        shutil.rmtree(SCR)
    for rel in NEEDED:
        dst = SCR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, dst)


def run():
    out = subprocess.run(
        [sys.executable, str(REPO / "tools/check_registration.py"),
         "--stage", "prereg", "--root", str(SCR)],
        capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    block, keep = [], False
    for line in out.split("\n"):
        if line.startswith("[") and "hash_set_single_source" in line:
            keep = True
        elif line.startswith("["):
            keep = False
        if keep:
            block.append(line)
    fails = [l for l in block if l.strip() and "note:" not in l and not l.startswith("[")]
    return ("FAIL" in (block[0] if block else "")), fails


def mutate(rel, old, new, count=1):
    p = SCR / rel
    s = p.read_text(encoding="utf-8")
    if count is None:                      # replace every occurrence
        assert s.count(old) > 0, "mutation anchor %r matched 0" % old[:50]
        p.write_text(s.replace(old, new), encoding="utf-8")
        return
    assert s.count(old) == count, "mutation anchor %r matched %d" % (old[:50], s.count(old))
    p.write_text(s.replace(old, new, 1), encoding="utf-8")


MUTATIONS = [
    ("M1  D1  a count literal made wrong (SIX -> SEVEN)",
     lambda: mutate("AVAILABILITY_DECLARATION.md",
                    "the `prereg-v30a` tag message carries SIX hashes",
                    "the `prereg-v30a` tag message carries SEVEN hashes")),
    ("M2  D2  tag-message body reordered (declaration moved first)",
     lambda: mutate("evidence/ceremony/CEREMONY_COMMANDS.md",
                    "<64 hex>  PREREG.md\n<64 hex>  DESIGN.md",
                    "<64 hex>  AVAILABILITY_DECLARATION.md\n<64 hex>  PREREG.md\n<64 hex>  DESIGN.md")),
    ("M3  D2  an enumeration loses a member (DEVIATIONS_DRAFT drops the declaration)",
     lambda: mutate("evidence/ceremony/DEVIATIONS_DRAFT.md",
                    "  `AVAILABILITY_DECLARATION.md` \u2014 computed at tag time",
                    "  \u2014 computed at tag time")),
    ("M4  D3  the staging plan drops a hashed file",
     lambda: mutate("evidence/ceremony/COMMIT_PLAN.md",
                    "git add tools/check_registration.py protocol/runtime_reference.py",
                    "git add protocol/runtime_reference.py")),
    ("M5a D4  the plan stops DERIVING $FILES from its authority",
     lambda: mutate("evidence/ceremony/COMMIT_PLAN.md",
                    "grep -m1 '^FILES=' evidence/ceremony/CEREMONY_COMMANDS.md",
                    "cat /dev/null   # restated below, not derived")),
    ("M5b D4  a hashed file is never named anywhere in the plan",
     lambda: mutate("evidence/ceremony/COMMIT_PLAN.md",
                    "protocol/runtime_reference.py",
                    "protocol/OTHER.py", count=None)),
    ("M6  D5  an exempted line DRIFTS (pin text altered)",
     lambda: mutate("AVAILABILITY_DECLARATION.md",
                    "The `prereg-v30` tag message carries **five** SHA-256 lines",
                    "The v30 tag message has **five** SHA-256 lines")),
    ("M7  authority deleted entirely",
     lambda: mutate("evidence/ceremony/CEREMONY_COMMANDS.md",
                    'FILES="PREREG.md', '#FILES="PREREG.md')),
]

print("=== BASELINE (unmutated scratch copy) ===")
fresh()
failed, fails = run()
print("   verdict: %s   failures: %d" % ("FAIL" if failed else "PASS", len(fails)))
assert not failed, "baseline must PASS or the battery proves nothing"
print()

results = []
for name, fn in MUTATIONS:
    fresh()
    try:
        fn()
    except AssertionError as exc:
        print("  %-62s ANCHOR MISS: %s" % (name, exc)); results.append((name, None)); continue
    failed, fails = run()
    results.append((name, failed))
    print("  %-62s %s" % (name, "FIRED" if failed else "*** SILENT ***"))
    for f in fails[:2]:
        print("        %s" % f.strip()[:150])

print()
caught = sum(1 for _, r in results if r)
print("MUTATIONS CAUGHT: %d / %d" % (caught, len(results)))
if SCR.exists():
    shutil.rmtree(SCR)
