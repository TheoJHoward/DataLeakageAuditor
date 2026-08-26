#!/usr/bin/env python3
"""B1.3 — for EVERY exemption, write a NEW wrong value onto the exempted line.

Reported per-exemption. The prior 8/8 and 5/5 batteries prove nothing about this
class: their mutations predate the failure mode, which is that a line-scoped
exemption swallows values it never whitelisted.

Method: for each exemption, mutate ONLY that line, appending a value the exemption
does not list, and confirm the check fires AT THAT SITE.
"""
import re, shutil, subprocess, sys, pathlib

ROOT = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
SCR = pathlib.Path("C:/Users/ttbea/AppData/Local/Temp/claude/"
                   "C--Users-ttbea-OneDrive-Desktop-MBO-2025-4mon--2026-01/"
                   "33e8c843-30fa-4bfb-aa9f-814c77bdb2e6/scratchpad/exmut")
NEED = ["AVAILABILITY_DECLARATION.md", "PREREG.md", "DESIGN.md", "HISTORY.md",
        "README.md", "PRACTICES.md", "PRIOR_ART_VERIFICATION.md",
        "evidence/ceremony/CEREMONY_COMMANDS.md", "evidence/ceremony/COMMIT_PLAN.md",
        "evidence/ceremony/DEVIATIONS_DRAFT.md", "evidence/ceremony/H34_DRAFT.md",
        "evidence/author_review/READ_THROUGH_PACKAGE.md",
        "evidence/fixture_spike/f4/DECLARATION_POINTER.md",
        "evidence/fixture_spike/f5/v30a_ceremony_CHECKLIST.md",
        "evidence/amendment/K1_SCHEMA_CLAUSES.md",
        "evidence/amendment/DECLARATION_SCRUB_LIST.md",
        "evidence/amendment/SCHEMA_SET_FINAL.md",
        "evidence/amendment/README.md"]

src = (ROOT / "tools/check_registration.py").read_text(encoding="utf-8")
KEY = re.compile(r'\("([^"]+)", (\d+)\): \(', re.M)


def table(name):
    m = re.search(r"^%s = \{(.*?)^\}" % name, src, re.S | re.M)
    return [(p, int(n)) for p, n in KEY.findall(m.group(1))] if m else []


D1 = table("_HASH_SET_EXEMPT")
D2 = table("_HASH_SET_ENUM_EXEMPT")
D7 = table("_D7_EXEMPT")


def fresh():
    if SCR.exists():
        shutil.rmtree(SCR)
    for rel in NEED:
        dst = SCR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)


def run(check):
    out = subprocess.run(
        [sys.executable, str(ROOT / "tools/check_registration.py"),
         "--stage", "prereg", "--root", str(SCR)],
        capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    keep, blk = False, []
    for line in out.split("\n"):
        if line.startswith("[") and check in line:
            keep = True
        elif line.startswith("["):
            keep = False
        if keep:
            blk.append(line)
    return [l for l in blk if l.strip() and "note:" not in l and not l.startswith("[")]


def poke(rel, lineno, suffix):
    p = SCR / rel
    L = p.read_text(encoding="utf-8", errors="replace").split("\n")
    L[lineno - 1] = L[lineno - 1] + suffix
    p.write_text("\n".join(L), encoding="utf-8")


print("B1.3 - ONE NEW-WRONG-VALUE MUTATION PER EXEMPTION\n")
rows, caught = [], 0

# D1: append a count the exemption does not whitelist ("nine hashes")
for rel, ln in D1:
    fresh()
    poke(rel, ln, "  (and nine hashes)")
    hits = [f for f in run("hash_set_single_source") if f.strip().startswith("%s:%d:" % (rel, ln))]
    ok = bool(hits)
    caught += ok
    rows.append(("D1", rel, ln, ok, hits[0].strip()[:96] if hits else ""))

# D2: append a path this site's whitelist does NOT already contain, so the
# mutation genuinely introduces a new value rather than restating a listed one.
FILES = re.search(r'^FILES="([^"]+)"',
                  (ROOT / "evidence/ceremony/CEREMONY_COMMANDS.md").read_text(encoding="utf-8"),
                  re.M).group(1).split()
for rel, ln in D2:
    fresh()
    window = " ".join((SCR / rel).read_text(encoding="utf-8", errors="replace")
                      .split("\n")[max(0, ln - 2): ln + 3])
    extra = next((f for f in FILES if f not in window), FILES[-1])
    poke(rel, ln, " " + extra)
    hits = [f for f in run("hash_set_single_source") if f.strip().startswith("%s:%d:" % (rel, ln))]
    ok = bool(hits)
    caught += ok
    rows.append(("D2", rel, ln, ok, hits[0].strip()[:96] if hits else ""))

# D7: append a hash and a size the exemption does not list
for rel, ln in D7:
    fresh()
    poke(rel, ln, " AVAILABILITY_DECLARATION.md `cafebabecafebabe` 424242 bytes")
    hits = [f for f in run("declaration_values") if f.strip().startswith("%s:%d:" % (rel, ln))]
    ok = bool(hits)
    caught += ok
    rows.append(("D7", rel, ln, ok, hits[0].strip()[:96] if hits else ""))

for det, rel, ln, ok, msg in rows:
    print("  %-3s %-46s %-5s %s" % (det, rel.split("/")[-1], ln,
                                    "FIRED" if ok else "*** SILENT ***"))
    if msg:
        print("        %s" % msg)

print("\n  PER-EXEMPTION MUTATIONS: %d / %d caught" % (caught, len(rows)))
shutil.rmtree(SCR, ignore_errors=True)
