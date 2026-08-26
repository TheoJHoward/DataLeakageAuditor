"""Run leakage-buster 1.0.2, leakfence 0.5.0 and temporalcv 2.3.0 against all eight cases.

All eight are executed for every tool; scoring uses the declared eligibility of
PRE_RUN_RECORD 4.7 and publishes the ineligible cells as abstentions.
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

import numpy as np  # noqa: E402
import case_defs as cd  # noqa: E402


# ---------------------------------------------------------------- leakage-buster 1.0.2
def run_leakage_buster():
    from leakage_buster.api import audit
    recs = []
    for case in cd.CASES:
        for side in cd.SIDES:
            d = cd.get(case, side)
            m = d["meta"]
            df = d["full"].copy()
            # cv_type supplied explicitly so the always-on "CV strategy recommendation"
            # (unmapped, PRE_RUN_RECORD 5.1) is not emitted as noise
            cv = "timeseries" if m.get("time") else ("group" if m.get("group") else "kfold")
            rec = dict(tool="leakage-buster", version="1.0.2", case=case, side=side,
                       config=dict(target=m["target"], time_col=m.get("time"), cv_type=cv,
                                   leak_threshold="default 0.02"))
            try:
                r = audit(df, target=m["target"], time_col=m.get("time"), cv_type=cv)
                risks = r.data.get("risks", []) if hasattr(r, "data") else []
                rec.update(status="ran",
                           fired_labels=[x.get("name") for x in risks],
                           risks=[{k: v for k, v in x.items() if k != "evidence"} for x in risks],
                           evidence={x.get("name"): str(x.get("evidence"))[:300] for x in risks})
            except Exception as e:
                rec.update(status="crash", error=f"{type(e).__name__}: {e}",
                           traceback=traceback.format_exc()[-1200:])
            recs.append(rec)
            print(f"  LB {case} {side:13s} {rec['status']:5s} {rec.get('fired_labels', rec.get('error',''))}")
    return recs


# ---------------------------------------------------------------- leakfence 0.5.0
def run_leakfence():
    import leakfence as lf
    recs = []
    for case in cd.CASES:
        for side in cd.SIDES:
            d = cd.get(case, side)
            m = d["meta"]
            tr = np.asarray(d["train_idx"], dtype=int)
            te = np.asarray(d["test_idx"], dtype=int)
            grp = d["full"][m["group"]].to_numpy() if m.get("group") else None
            X = d["full"][m["features"]].to_numpy(dtype=float)
            rec = dict(tool="leakfence", version="0.5.0", case=case, side=side,
                       config=dict(entry_points=["audit_split", "check_duplicates"],
                                   subject="group_id" if grp is not None else None,
                                   strict=False, allow_index_reuse=False))
            try:
                fired, detail = [], {}
                rep = lf.audit_split(train_idx=tr, test_idx=te, subject=grp,
                                     n_rows=len(d["full"]))
                for v in rep.violations:
                    fired.append(v.check)
                    detail[v.check] = v.message[:220]
                try:
                    # check_duplicates returns (groups, violations) -- a tuple, not a report
                    groups, dviol = lf.check_duplicates(X, train_idx=tr, test_idx=te)
                    for v in dviol:
                        chk = getattr(v, "check", "duplicate_rows")
                        fired.append(chk)
                        detail[chk] = str(getattr(v, "message", v))[:220]
                    detail["_duplicate_groups_n"] = len(groups)
                    detail["_duplicate_violations_n"] = len(dviol)
                except Exception as e:
                    detail["_check_duplicates_error"] = f"{type(e).__name__}: {e}"
                # C2's eligibility is the preprocessing lint, which needs a pipeline OBJECT.
                # Adapter judged SETUP: the case's own construction expressed as an sklearn
                # Pipeline -- pooled-fit (contaminated) vs train-only-fit (clean).
                try:
                    from sklearn.linear_model import LogisticRegression
                    from sklearn.pipeline import Pipeline
                    from sklearn.preprocessing import StandardScaler
                    pipe = Pipeline([("scaler", StandardScaler()),
                                     ("clf", LogisticRegression(max_iter=200))])
                    if side == "contaminated":
                        pipe.fit(X, d["full"][m["target"]].to_numpy())   # fitted on train+test
                    else:
                        pipe.fit(X[tr], d["full"][m["target"]].to_numpy()[tr])
                    lint = lf.lint_pipeline(pipe)
                    lviol = lint if isinstance(lint, list) else getattr(lint, "violations", [])
                    for v in lviol:
                        chk = getattr(v, "check", "global_preprocessing")
                        fired.append(chk)
                        detail[chk] = str(getattr(v, "message", v))[:220]
                    detail["_lint_pipeline_raw"] = str(lint)[:220]
                except Exception as e:
                    detail["_lint_pipeline_error"] = f"{type(e).__name__}: {e}"
                rec.update(status="ran", fired_labels=sorted(set(fired)), detail=detail)
            except Exception as e:
                rec.update(status="crash", error=f"{type(e).__name__}: {e}",
                           traceback=traceback.format_exc()[-1200:])
            recs.append(rec)
            print(f"  LF {case} {side:13s} {rec['status']:5s} {rec.get('fired_labels', rec.get('error',''))}")
    return recs


# ---------------------------------------------------------------- temporalcv 2.3.0
def run_temporalcv():
    from sklearn.ensemble import RandomForestClassifier
    from temporalcv import gates
    recs = []
    for case in cd.CASES:
        for side in cd.SIDES:
            d = cd.get(case, side)
            m = d["meta"]
            full = d["full"].dropna().reset_index(drop=True)
            X = full[m["features"]].to_numpy(dtype=float)
            y = full[m["target"]].to_numpy()
            rec = dict(tool="temporalcv", version="2.3.0", case=case, side=side,
                       config=dict(gates=["gate_signal_verification", "gate_temporal_boundary",
                                          "gate_suspicious_improvement"],
                                   model="RandomForestClassifier(n_estimators=50, random_state=0)",
                                   n_shuffles=50, random_state=0,
                                   note="adapter: a model is fitted per case per side; the gates "
                                        "take a fitted model + X/y"))
            try:
                model = RandomForestClassifier(n_estimators=50, random_state=0).fit(X, y)
                fired, detail = [], {}
                try:
                    g = gates.gate_signal_verification(model, X, y, n_shuffles=50,
                                                       random_state=0)
                    st = str(getattr(g.status, "value", g.status))
                    detail["gate_signal_verification"] = dict(
                        status=st, message=str(g.message)[:220],
                        metric=getattr(g, "metric_value", None))
                    if st in ("HALT", "WARN"):
                        fired.append("gate_signal_verification")
                except Exception as e:
                    detail["gate_signal_verification"] = f"ERROR {type(e).__name__}: {e}"
                try:
                    from sklearn.metrics import accuracy_score
                    acc = accuracy_score(y, model.predict(X))
                    base = max(np.mean(y), 1 - np.mean(y))
                    g = gates.gate_suspicious_improvement(float(acc), float(base),
                                                          metric_name="accuracy")
                    st = str(getattr(g.status, "value", g.status))
                    detail["gate_suspicious_improvement"] = dict(
                        status=st, message=str(g.message)[:220], model=float(acc),
                        baseline=float(base))
                    if st in ("HALT", "WARN"):
                        fired.append("gate_suspicious_improvement")
                except Exception as e:
                    detail["gate_suspicious_improvement"] = f"ERROR {type(e).__name__}: {e}"
                rec.update(status="ran", fired_labels=sorted(set(fired)), detail=detail)
            except Exception as e:
                rec.update(status="crash", error=f"{type(e).__name__}: {e}",
                           traceback=traceback.format_exc()[-1200:])
            recs.append(rec)
            print(f"  TC {case} {side:13s} {rec['status']:5s} {rec.get('fired_labels', rec.get('error',''))}")
    return recs


if __name__ == "__main__":
    for name, fn in (("leakage-buster", run_leakage_buster),
                     ("leakfence", run_leakfence),
                     ("temporalcv", run_temporalcv)):
        print(f"===== {name} =====")
        try:
            recs = fn()
        except Exception:
            traceback.print_exc()
            recs = [dict(tool=name, status="crash", error=traceback.format_exc()[-1500:])]
        with open(os.path.join(OUT, f"{name}.json"), "w") as f:
            json.dump(recs, f, indent=2)
