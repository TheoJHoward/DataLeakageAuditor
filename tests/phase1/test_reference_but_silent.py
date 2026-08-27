"""The reference-but-silent screen, against a source with KNOWN answers.

WHY A TEST AND NOT JUST A RUN. The screen's whole value is that it separates
three things a silent cohort can mean, and its first version could not: a
genuine `aggressor_side`-class dependency, a NAME COLLISION with another
frame's column of the same name, and ordinary silence. The first version
reported `trades.side` and `trades.action` as candidates on the strength of
`df["side"]` and `df["action"]` inside a function that reads an entirely
different parquet. A screen that cannot tell those apart hands a reader two
false leads for every true one.

So the synthetic source below contains all three cases deliberately, and the
test asserts the screen assigns each to the right bucket.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

SCRIPT = pathlib.Path(__file__).resolve().parent / "reference_but_silent.py"

SOURCE = '''"""A synthetic builder with one of each case."""
import pandas as pd


def load_other(path):
    # A DIFFERENT frame that happens to share a column name with `trades`.
    df = pd.read_parquet(path, columns=["side", "ts"])
    df["is_bid"] = df["side"].isin(["B"])
    return df.groupby("ts").agg(n=("is_bid", "sum")).reset_index()


def build_features(trades, snap):
    # Read but by a predicate that is false for every row -- the class.
    is_buy = trades["aggressor_side"].isin(["B", "Buy", "buy"])
    trades["signed"] = is_buy.astype(int)
    # Genuinely read and genuinely moves the output.
    out = snap[["mid_price"]].copy()
    out["signed"] = trades["signed"].to_numpy()
    return out
'''
# Padded past the screen's minimum-size guard, which exists to catch a
# truncated or wrong source file rather than to police style.
SOURCE = SOURCE + "\n".join("# pad %d" % i for i in range(120))


def _run(tmp_path, silent, fired):
    src = tmp_path / "builder.py"
    src.write_text(SOURCE, encoding="utf-8")
    res = tmp_path / "merged.json"
    res.write_text(json.dumps({
        "dependency_map": {c: ["out"] for c in fired},
        "silent_cohorts": silent,
    }), encoding="utf-8")
    out = subprocess.run([sys.executable, str(SCRIPT), str(src), str(res)],
                         capture_output=True, text=True, timeout=180)
    assert out.returncode == 0, out.stdout + out.stderr
    return out.stdout


def test_screen_separates_the_class_from_a_name_collision(tmp_path):
    text = _run(tmp_path,
                silent=["col:trades.aggressor_side", "col:trades.side",
                        "col:trades.order_id"],
                fired=["col:snap.mid_price"])

    # Whitespace-insensitive: the test is about the CLASSIFICATION, not about
    # the report's column padding. Pinning the padding makes a cosmetic change
    # look like a regression, which trains a reader to ignore this test.
    flat = " ".join(text.split())
    assert "SAME-FRAME candidates : 1" in flat, text
    assert "name collisions : 1" in flat, text
    assert "unreferenced : 1" in flat, text

    # the class member is named for a human to read
    assert "** col:trades.aggressor_side -- READ THE PREDICATE." in text
    # the collision is reported, not counted
    assert "col:trades.side" in text
    assert "name collision" in text
    assert "** col:trades.side" not in text


def test_screen_halts_rather_than_returning_an_empty_list(tmp_path):
    """An empty screen is not an empty finding.

    Pointed at a stub, the screen must refuse. Silently returning "no
    candidates" from the wrong file is indistinguishable from a clean result,
    and that is the shape of answer this whole suite exists to refuse.
    """
    src = tmp_path / "stub.py"
    src.write_text("x = 1\n", encoding="utf-8")
    res = tmp_path / "merged.json"
    res.write_text(json.dumps({"dependency_map": {}, "silent_cohorts": ["col:a.b"]}),
                   encoding="utf-8")
    out = subprocess.run([sys.executable, str(SCRIPT), str(src), str(res)],
                         capture_output=True, text=True, timeout=180)
    assert out.returncode != 0
    assert "HALT" in out.stdout + out.stderr


def test_screen_halts_when_no_cohorts_were_read(tmp_path):
    src = tmp_path / "builder.py"
    src.write_text(SOURCE, encoding="utf-8")
    res = tmp_path / "merged.json"
    res.write_text(json.dumps({"dependency_map": {}, "silent_cohorts": []}),
                   encoding="utf-8")
    out = subprocess.run([sys.executable, str(SCRIPT), str(src), str(res)],
                         capture_output=True, text=True, timeout=180)
    assert out.returncode != 0
    assert "HALT" in out.stdout + out.stderr
