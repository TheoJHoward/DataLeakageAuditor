#!/usr/bin/env python3
"""§37 — close the manifest's reverse direction.

`sha256sum -c` walks the manifest and checks each listed path against disk. It has
no way to notice a file that is ON DISK but NOT LISTED - that file ships inside the
signed commit with nothing attesting its content, and every existing check passes.

D9 asserts the other direction. A ceremony step C2d-1 does the same against the
INDEX at tag time, because that is the set the commit will actually carry.
"""
import pathlib

TOOL = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                    "tools/check_registration.py")
s = TOOL.read_text(encoding="utf-8")

D9 = '''
# ---------------------------------------------------------------------------
# D9 (R71/§37) - the manifest's REVERSE direction.
#
# `sha256sum -c MANIFEST.sha256` verifies listed -> disk. It is structurally
# blind to disk -> listed: a file added to the evidence tree without a manifest
# line is invisible to it, and would ship inside the signed commit unattested
# while every check reports OK.
#
# B6 recorded that the two sets happened to coincide (248/248) - a fact about
# that day's contents, not a property of the check. This makes it a property.
# ---------------------------------------------------------------------------

_MANIFEST_REL = "evidence/MANIFEST.sha256"
# Repository-root files the manifest claims via `../` lines. Derived from the
# manifest itself, not restated here.
_MANIFEST_LINE = re.compile(r"^[0-9a-f]{64}  (.+)$", re.M)


def check_manifest_covers_tree(root: Path) -> list[Finding]:
    """D9 - every file in the manifest's claimed scope HAS a manifest line."""
    man = root / _MANIFEST_REL
    if not man.exists():
        return [Finding("manifest_coverage", _MANIFEST_REL, None,
                        "the manifest is missing; nothing attests the evidence tree")]
    listed = set(_MANIFEST_LINE.findall(man.read_text(encoding="utf-8", errors="replace")))
    in_tree = {p for p in listed if not p.startswith("../")}
    up_lines = {p[3:] for p in listed if p.startswith("../")}

    ev = root / "evidence"
    on_disk = {q.relative_to(ev).as_posix() for q in ev.rglob("*") if q.is_file()}
    on_disk.discard("MANIFEST.sha256")          # the manifest cannot list itself

    findings = [Finding("manifest_coverage", _MANIFEST_REL, None,
                        "scope: %d in-tree lines + %d `../` lines; %d files on disk"
                        % (len(in_tree), len(up_lines), len(on_disk)), is_note=True)]

    unlisted = sorted(on_disk - in_tree)
    if unlisted:
        findings.append(Finding(
            "manifest_coverage", _MANIFEST_REL, None,
            "D9: %d file(s) in the evidence tree have NO manifest line and would "
            "ship inside the signed commit unattested: %s. `sha256sum -c` cannot "
            "see this - it only walks what the manifest lists."
            % (len(unlisted), ", ".join(unlisted[:8]) + (" ..." if len(unlisted) > 8 else ""))))
    missing = sorted(in_tree - on_disk)
    if missing:
        findings.append(Finding(
            "manifest_coverage", _MANIFEST_REL, None,
            "D9: the manifest lists %d path(s) that are not on disk: %s"
            % (len(missing), ", ".join(missing[:8]))))
    for rel in sorted(up_lines):
        if not (root / rel).exists():
            findings.append(Finding(
                "manifest_coverage", _MANIFEST_REL, None,
                "D9: the manifest claims repository-root file %r, which does not exist" % rel))
    if not unlisted and not missing:
        findings.append(Finding(
            "manifest_coverage", _MANIFEST_REL, None,
            "D9: manifest coverage is EXACT in both directions (%d files)" % len(on_disk),
            is_note=True))
    return findings

'''

ANCHOR = "def check_phase_arithmetic(root: Path) -> list[Finding]:"
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, D9.lstrip("\n") + "\n" + ANCHOR, 1)
REG = '    ("prereg", "line_citations", check_line_citations),\n'
assert s.count(REG) == 1
s = s.replace(REG, REG + '    ("prereg", "manifest_coverage", check_manifest_covers_tree),\n', 1)
TOOL.write_text(s, encoding="utf-8")
import ast
ast.parse(TOOL.read_text(encoding="utf-8"))
print("D9 installed and registered; syntax OK")

# ---- the ceremony step, against the INDEX -------------------------------
CC = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01/"
                  "evidence/ceremony/CEREMONY_COMMANDS.md")
c = CC.read_text(encoding="utf-8")
EM = "\u2014"
OLD = "# C2d " + EM + " the evidence manifest verifies against the tree about to be committed"
NEW = ('# C2d-1 ' + EM + ' REVERSE DIRECTION. Run BEFORE C2d.\n'
       '#   `sha256sum -c` walks the MANIFEST and checks each listed path against disk.\n'
       '#   It cannot see a file that is STAGED BUT NOT LISTED. Such a file ships inside\n'
       '#   the signed commit with nothing attesting its bytes, and C2d still reports OK.\n'
       'git diff --cached --name-only -- evidence \\\n'
       '  | sed \'s|^evidence/||\' | grep -v \'^MANIFEST\\.sha256$\' | sort > /tmp/_staged.$$\n'
       'grep -oE \'^[0-9a-f]{64}  .+$\' evidence/MANIFEST.sha256 \\\n'
       '  | sed \'s/^[0-9a-f]\\{64\\}  //\' | grep -v \'^\\.\\./\' | sort > /tmp/_listed.$$\n'
       'unlisted=$(comm -23 /tmp/_staged.$$ /tmp/_listed.$$)\n'
       'rm -f /tmp/_staged.$$ /tmp/_listed.$$\n'
       'if [ -n "$unlisted" ]; then\n'
       '  echo "C2d-1 FAILED ' + EM + ' staged but NOT in the manifest, would ship unattested:"\n'
       '  printf \'%s\\n\' "$unlisted"; exit 1\n'
       'fi\n'
       'echo "C2d-1 OK ' + EM + ' every staged evidence file has a manifest line"\n'
       '\n'
       + OLD)
assert c.count(OLD) == 1, "C2d anchor %d" % c.count(OLD)
CC.write_text(c.replace(OLD, NEW, 1), encoding="utf-8")
print("CEREMONY_COMMANDS.md: C2d-1 added before C2d")
