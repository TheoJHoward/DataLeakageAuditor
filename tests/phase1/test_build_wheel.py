"""The build tool takes the sdist route and clears the tree first. R276 §1(5).

The wheel check could not fail while `build/lib` survived between builds, so the
tool that builds the wheel for verification does two things the old command did
not: it removes `build/` and announces what it removed, and it builds the wheel
FROM an sdist rather than from the working tree.

The build itself is not run here -- it is minutes and a network -- and the round
runs it. What is pinned here is the housekeeping, the route, and the file list.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(ROOT / "tools")):
    if p not in sys.path:
        sys.path.insert(0, p)

import build_wheel                                              # noqa: E402


def test_the_HOUSEKEEPING_removes_the_tree_and_COUNTS_it(tmp_path, capsys):
    tree = tmp_path / "build" / "lib" / "leakaudit" / "templates"
    tree.mkdir(parents=True)
    (tree / "TEMPLATE.json").write_text("{}", encoding="utf-8")
    (tmp_path / "build" / "lib" / "leakaudit" / "cli.py").write_text(
        "", encoding="utf-8")
    assert build_wheel.clean_build_tree(tmp_path) == 2
    assert not (tmp_path / "build").exists()
    out = capsys.readouterr().out
    assert "removed build/ -- 2 file(s)" in out, out
    assert "D-V30A-122" in out, "the deletion carries why it happens"


def test_it_says_so_when_there_is_NOTHING_to_remove(tmp_path, capsys):
    assert build_wheel.clean_build_tree(tmp_path) == 0
    assert "nothing to remove" in capsys.readouterr().out


def test_the_FILE_LIST_is_the_wheel_s_own(tmp_path):
    whl = tmp_path / "x-0.1-py3-none-any.whl"
    with zipfile.ZipFile(whl, "w") as z:
        z.writestr("leakaudit/cli.py", "x = 1\n")
        z.writestr("leakaudit/templates/TEMPLATE.json", "{}")
    assert build_wheel.file_list(whl) == ["leakaudit/cli.py",
                                          "leakaudit/templates/TEMPLATE.json"]


def test_the_ROUTE_is_the_sdist_one_and_NOT_an_in_tree_wheel():
    src = (ROOT / "tools" / "build_wheel.py").read_text(encoding="utf-8")
    assert '"-m", "build"' in src, "the sdist route"
    assert "pip wheel" not in src.split('"""', 2)[2], (
        "an in-tree `pip wheel .` inherits build/lib, which is the defect this "
        "tool exists for")
