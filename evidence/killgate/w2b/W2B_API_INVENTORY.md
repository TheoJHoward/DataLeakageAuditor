# W2b step 1 — the comparators are reachable, and their entry points are intact

**§9.2's first question is not "what did the tools report" but "can they be called at all."** This
records the answer, derived by importing each package **in its own virtualenv** and reading its
public surface — not from the k6 harness, which is two rounds old, and not from memory.

**Why that mattered before it was checked.** W2b exists because k6's nulls were uninterpretable:
*"A tool that has never been shown to fire through its adapter has not been tested; it has been
mishandled."* A control written against an API that has moved fails for the wrong reason, and a
control failing for the wrong reason is precisely what would be mistaken for a tool that does not
fire.

## The environment

The comparators are **not importable from the main interpreter, by design** — they carry conflicting
`pandas` and `scikit-learn` pins. Each is invoked through its own venv's interpreter, as k6's
runners did.

| venv | tool | version | entry points k6 used | intact? |
|---|---|---|---|---|
| `general` | `leakage-buster` | **1.0.2** | `api.audit(df, target, time_col, cv_type)` | **yes** |
| `general` | `leakfence` | **0.5.0** | `audit_split`, `check_duplicates`, `lint_pipeline` | **yes** |
| `general` | `temporalcv` | **2.3.0** | `gates.gate_residual_diagnostics`, `gate_signal_verification`, `gate_suspicious_improvement` | **yes** |
| `general` | `Leakly` | **0.1.2** | `MLPipeline`, `permute_label`, `load_example_leakage_config` | **yes** |
| `ld` | `leak-detect` | 0.0.1 *(declares no `__version__`)* | `detect_horizontal_leakage`, `detect_vertical_leakage` | **yes** |
| `dc` | `deepchecks` | **0.19.1** | `Dataset`, `suites.data_integrity`, `suites.train_test_validation` | **yes** |

**All six import. No entry point has moved.** The versions match `evidence/killgate/k6/env/VERSIONS.txt`,
captured 14 Aug 2026 *before results were read*.

**Not runnable, and why — unchanged from k6 and not a new finding:** `leakr` and `bioLeak` are R
packages and **R is not installed**; `leakage-analysis` needs `souffle`, also absent;
`LeakageDetector` is a VS Code extension with no headless entry point. Those four are abstentions on
scope grounds, recorded at k6 and not re-litigated here.

## What the probe found that changes the plan

**Leakly ships BOTH fixtures.** `load_example_leakage_config()` — the one W2b names — **and**
`load_example_nonleakage_config()`. That is a vendor-supplied **positive and negative pair**, which
is stronger than a positive alone: a tool that fires on both is not discriminating, and only the
pair can show that.

**`temporalcv.gates` is a module, not a callable.** Its three gates are
`gate_residual_diagnostics`, `gate_signal_verification`, `gate_suspicious_improvement`.
**`gate_suspicious_improvement` is the one k6 got wrong** — W2b's defect #7 records that it was fed
an **accuracy** where the gate's formula expects an **error** metric, so a mapped gate silently
never fired. The control for this tool must pass an error metric, and must show the gate firing
before any null from it is interpretable.

## What this does NOT establish

**Nothing about whether any tool detects anything.** This is reachability only. W2b step 2 — each
adapter demonstrated to fire on a case the tool's own documentation says it catches, *through the
same adapter and invocation path the real run uses* — is the next item, and until it passes for a
given tool, **that tool's result on the acceptance fixture is `uninterpretable`, not a null**.

Derived by `probe_apis.py`, which imports each package and prints its surface; it asserts nothing it
did not read.
