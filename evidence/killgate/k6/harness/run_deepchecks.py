"""Run deepchecks 0.19.1 against the eligible cases.

Eligible per PRE_RUN_RECORD 4.7: C1, C4, C5, C6, C8. All eight are executed; scoring uses the
declared eligibility only, and the ineligible cells are published as abstentions.

Both the train_test_validation and data_integrity suites are run, so the tool gets its widest
shot. deepchecks' own not-run accounting (SuiteResult.get_not_ran_checks / CheckFailure) is
captured verbatim -- it is the roster's only explicit executed/not-run accounting and is the
evidence for 10.1 criterion 2.
"""
import json
import os
import sys
import traceback
import warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.abspath(os.path.join(HERE, "..", "raw"))

import case_defs as cd  # noqa: E402
from deepchecks.core import CheckFailure  # noqa: E402
from deepchecks.tabular import Dataset  # noqa: E402
from deepchecks.tabular.suites import data_integrity, train_test_validation  # noqa: E402


def build_datasets(d):
    """Adapter, judged SETUP under CROSS_TOOL_COMPARISON 2.6 item 4.

    `row_id` carries each row's position in `full` -- i.e. the case's declared split restated in
    the input form deepchecks reads. Without it, `Index Train Test Leakage` (the check 2.5 maps to
    T1) and `Identifier Label Correlation` cannot run at all. Supplying it is the same reshaping
    the leakfence index-array adapter performs, and it can only help the tool.
    """
    full, m = d["full"], d["meta"]
    f = full.copy()
    f["row_id"] = range(len(f))
    tr = f.iloc[d["train_idx"]].reset_index(drop=True)
    te = f.iloc[d["test_idx"]].reset_index(drop=True)
    kw = dict(label=m["target"], cat_features=[], index_name="row_id")
    if m.get("time"):
        kw["datetime_name"] = m["time"]
    return Dataset(tr, **kw), Dataset(te, **kw)


def summarize(res):
    """One record per check: did it run, and did any condition fail (= the tool fired)."""
    out = []
    for r in res.results:
        if isinstance(r, CheckFailure):
            out.append(dict(check=r.check.name(), ran=False, fired=None,
                            error=f"{type(r.exception).__name__}: {r.exception}"))
            continue
        conds = []
        fired = False
        for c in getattr(r, "conditions_results", []) or []:
            # ConditionResult.is_pass is a METHOD, not a property: bool(c.is_pass) is always True
            # and would have silently reported "deepchecks never fires" for every case.
            # Read the category directly.
            cat = str(getattr(c.category, "value", c.category))
            passed = cat == "PASS"
            conds.append(dict(name=c.name, category=cat, passed=passed,
                              details=str(c.details)[:400]))
            if not passed:
                fired = True
        # The check VALUE is captured as well as the condition verdict. Scoring uses the generous
        # predicate of PRE_RUN_RECORD 6.2: a check counts as having fired if its condition failed
        # OR its value reports a non-null detection of the case's type. Capturing the value is
        # what makes the generous reading auditable rather than asserted.
        try:
            val = json.loads(json.dumps(r.value, default=str))
        except Exception as e:
            val = f"<unserialisable: {e}>"
        out.append(dict(check=r.check.name(), ran=True, fired=fired, conditions=conds,
                        value=val, has_display=bool(getattr(r, "display", None))))
    return out


def main():
    records = []
    for case in cd.CASES:
        for side in cd.SIDES:
            d = cd.get(case, side)
            rec = dict(tool="deepchecks", version="0.19.1", case=case, side=side,
                       config=dict(suites=["train_test_validation", "data_integrity"],
                                   datetime_name=d["meta"].get("time"),
                                   index_name=d["meta"].get("group"),
                                   model="none supplied (checks needing a fitted model are "
                                         "reported by the tool as not-run)"))
            try:
                train, test = build_datasets(d)
                checks = []
                notrun = []
                for name, suite in (("train_test_validation", train_test_validation()),
                                    ("data_integrity", data_integrity())):
                    if name == "data_integrity":
                        res = suite.run(train)
                    else:
                        res = suite.run(train_dataset=train, test_dataset=test)
                    for c in summarize(res):
                        c["suite"] = name
                        checks.append(c)
                    try:
                        notrun += [f"{name}:{c.check.name()}"
                                   for c in res.get_not_ran_checks()]
                    except Exception as e:
                        notrun.append(f"{name}:<get_not_ran_checks failed: {e}>")
                rec.update(status="ran", checks=checks, not_ran=notrun,
                           fired_labels=sorted({c["check"] for c in checks if c.get("fired")}))
            except Exception as e:
                rec.update(status="crash", error=f"{type(e).__name__}: {e}",
                           traceback=traceback.format_exc()[-1500:])
            records.append(rec)
            print(f"{case} {side:13s} {rec['status']:5s} "
                  f"fired={rec.get('fired_labels', rec.get('error', ''))}")
    with open(os.path.join(OUT, "deepchecks.json"), "w") as f:
        json.dump(records, f, indent=2)


if __name__ == "__main__":
    main()
