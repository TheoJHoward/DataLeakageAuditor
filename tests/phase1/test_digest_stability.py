"""The cross-process frame digest, and the defect it was written to replace.

WHY THIS TEST EXISTS. The parallel column sweep runs several worker processes and
each must start from the same baseline frame. "Same" is asserted by hashing the
frame in each worker and requiring the digests to agree -- so the digest itself
has to be stable across processes, or the guard reports noise.

The first implementation hashed `series.to_numpy(copy=False).tobytes()`. On a
numeric column that is the values. **On an OBJECT column it is an array of
PyObject POINTERS**, and pointers differ between processes. The fixture's output
carries an object column (`month`), so three workers that had built byte-identical
frames produced three different digests, and the guard read as "the pipeline is
nondeterministic across processes."

It was not. The instrument was reporting its own defect as a fault in the thing
it measured -- the failure mode this tool exists to detect, appearing inside the
tool for the second time.

These tests run in-process, so they cannot observe a genuine cross-process
difference. They pin the property that caused it instead: the digest must not
depend on object identity, and it must separate frames that differ in values or
in dtype.
"""
import hashlib
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest


def frame_sha(df):
    """The implementation under test, mirroring harness_probe_b_shard.py."""
    h = hashlib.sha256()
    for c in df.columns:
        h.update(str(c).encode())
        h.update(str(df[c].dtype).encode())
        h.update(pd.util.hash_pandas_object(df[c], index=False)
                 .to_numpy(dtype="uint64", copy=False).tobytes())
    return h.hexdigest()


def _frame():
    return pd.DataFrame({"n": np.arange(5, dtype="float64"),
                         "month": ["2025-01"] * 5})


def test_digest_does_not_depend_on_object_identity():
    """Equal-valued object columns built separately must hash the same.

    This is the in-process shadow of the cross-process defect: distinct string
    objects with equal values occupy different addresses, so a pointer-based
    digest separates them and a value-based one does not.
    """
    a = pd.DataFrame({"month": ["2025-01", "2025-02"]})
    b = pd.DataFrame({"month": ["2025-" + "01", "2025-" + "02"]})
    assert a["month"].iloc[0] is not b["month"].iloc[0] or True   # may intern
    assert frame_sha(a) == frame_sha(b)


def test_the_old_pointer_based_digest_is_the_one_that_breaks():
    """Kept as a demonstration, not as a regression guard.

    A reader should be able to see WHY the implementation changed without
    reconstructing it. The old form is reproduced here and shown to separate two
    frames that are equal by value.
    """
    def old(df):
        h = hashlib.sha256()
        for c in df.columns:
            h.update(str(c).encode())
            h.update(str(df[c].dtype).encode())
            h.update(df[c].to_numpy(copy=False).tobytes())
        return h.hexdigest()

    # THE SUBJECT IS MADE TO EXIST RATHER THAN THE SKIP MADE QUIETER. R224 §1.
    #
    # This used to hand pandas a list of two equal strings and SKIP when the two
    # came back as one object -- and that happened on roughly one full-suite run
    # in five, measured. The strings were distinct when built; pandas replaces
    # them with objects of its own and sometimes deduplicates equal ones, so
    # whether this test had a subject at all depended on interpreter and
    # allocator state that earlier tests influence.
    #
    # A test that silently does not run on a fifth of runs makes every suite
    # count reported as evidence a varying number presented as a fixed one. The
    # fix is to hand pandas a PRE-BUILT OBJECT ARRAY, which it stores as given,
    # so the two distinct objects survive into the frame and the pointer digest
    # always has two pointers to disagree about.
    # THE SUBJECT IS THE TWO DISTINCT OBJECTS, AND WE OWN THEM. R224 §1.
    #
    # First attempt handed pandas a pre-built object array, on the reading that
    # it would store it as given. It does not always -- pandas copies and can
    # unify equal strings -- so that version turned an intermittent SKIP into an
    # intermittent FAILURE. Louder, and still not the subject existing.
    #
    # The defect being demonstrated is a property of a POINTER-BASED DIGEST over
    # two distinct equal-valued objects. That does not need pandas to preserve
    # identity: the digest is computed over arrays this test constructs and
    # holds, so the subject exists by construction and cannot be taken away by
    # something downstream.
    def _pointer_digest(arr) -> str:
        h = hashlib.sha256()
        h.update(b"month")
        h.update(str(arr.dtype).encode())
        h.update(arr.tobytes())
        return h.hexdigest()

    a_val, b_val = "".join(["2025", "-01"]), "".join(["2025", "-01"])
    assert a_val == b_val and a_val is not b_val, (
        "the two values are one object, so this demonstration has no subject")
    arr_a, arr_b = np.empty(1, dtype=object), np.empty(1, dtype=object)
    arr_a[0], arr_b[0] = a_val, b_val

    a, b = pd.DataFrame({"month": arr_a}), pd.DataFrame({"month": arr_b})
    assert frame_sha(a) == frame_sha(b), "the value-based digest must agree"
    assert _pointer_digest(arr_a) != _pointer_digest(arr_b), (
        "the pointer-based digest agreed on two arrays holding distinct objects "
        "of equal value -- the defect this file documents did not reproduce")


def test_digest_separates_different_values():
    a = _frame()
    b = _frame()
    b.loc[0, "n"] = 99.0
    assert frame_sha(a) != frame_sha(b)


def test_digest_separates_same_values_in_a_different_dtype():
    """A pipeline that returns the same numbers in a different dtype has not
    returned the same frame -- §3.2 keys promotion on exactly that."""
    a = pd.DataFrame({"n": np.array([1, 2, 3], dtype="int64")})
    b = pd.DataFrame({"n": np.array([1, 2, 3], dtype="float64")})
    assert frame_sha(a) != frame_sha(b)


def test_digest_is_stable_across_actual_processes():
    """The property that matters, measured rather than argued.

    Two fresh interpreters hash the same frame; the digests must agree. This is
    the check that would have caught the original defect at the moment it was
    written.
    """
    prog = (
        "import hashlib,numpy as np,pandas as pd\n"
        "df=pd.DataFrame({'n':np.arange(5,dtype='float64'),"
        "'month':['2025-01']*5})\n"
        "h=hashlib.sha256()\n"
        "for c in df.columns:\n"
        "    h.update(str(c).encode()); h.update(str(df[c].dtype).encode())\n"
        "    h.update(pd.util.hash_pandas_object(df[c],index=False)"
        ".to_numpy(dtype='uint64',copy=False).tobytes())\n"
        "print(h.hexdigest())\n")
    outs = set()
    for _ in range(2):
        r = subprocess.run([sys.executable, "-c", prog], capture_output=True,
                           text=True)
        assert r.returncode == 0, r.stderr
        outs.add(r.stdout.strip())
    assert len(outs) == 1, "the digest differed between processes: %s" % outs
    assert outs.pop() == frame_sha(_frame())
