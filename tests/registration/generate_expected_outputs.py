"""Generate EXPECTED_OUTPUTS.md from the canonical fixtures and the reducer.

The tests pin the reducer to hand-derived expectations first; this file then
renders what the reducer actually computes, so a human read reviews the same
numbers the suite enforces. Run:  python tests/registration/generate_expected_outputs.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for p in (str(ROOT), str(Path(__file__).resolve().parent)):
    if p not in sys.path:
        sys.path.insert(0, p)

from protocol.runtime_reference import (  # noqa: E402
    GateResult,
    SuppressedGate,
    SuppressedMetric,
    apply_runtime_gates,
    compute_runtime_metrics,
    derive_evidence_events,
    derive_reported_findings,
    evaluate_runtime_assertions,
    gate_id_for,
    resolve_state_pair,
)
from traces import ASSERTION_SCENARIOS, FIXTURES  # noqa: E402

OUT = Path(__file__).resolve().parent / "EXPECTED_OUTPUTS.md"

HEADER = """\
# EXPECTED_OUTPUTS — registration trace suite

**Generated from `tests/registration/traces.py` by
`generate_expected_outputs.py`. Do not edit by hand — regenerate.**

This is the artifact PREREG §6.6.1 puts first in the human read: the
expected outputs are derived by the author from the prose, so a misreading
can be encoded in both the reducer and this table. Reading it is the check
the machine cannot perform.

Every value below is also pinned by hand-derived expectations in
`traces.py`; `test_expected_outputs.py` fails if this file drifts from what
the reducer computes.

## Interpretation notes — all resolved as of v29

- **I1 (pair-level vs case-level denominators): confirmed.** PREREG §7.4
  (since v28) defines both denominators for every row including runtime:
  proof/evidence yield and the unprobed rate use the pair-level
  *scope-eligible* denominator, so labelled pairs from `not_applicable` and
  `unsupported` cases remain in them as misses (T14–T16); case-level rates
  use the *execution-eligible* membership of §7.7
  (`schedule_state ∈ {completed, incomplete}`).
- **I2 (short_circuited exclusion): confirmed.** `short_circuited` cases
  are excluded from every metric denominator including the pair-level ones
  (PREREG §6.6); they cannot arise in an evaluation run, so no published
  number depends on the exclusion (T08–T10).
- **I3 (unit grammar): resolved.** `feature` is in §7.0 rule 2's grammar
  (since v28), so feature discovery recall's unit is legal.
- **Canonized by v29:** the missing-trace protocol violation (§6.6's
  explicit-trace paragraph), the within-case scoring key with corpus-level
  case identity (§7.2), and the count-over-all-cases shape of the
  `not_applicable`/`unsupported`/`short_circuited` counts (§7.2.1) — the
  three decisions this suite previously carried as interpretation are now
  locked prose.
- **v30 suppression (§7.2.1).** A combination that is `not_applicable` on
  every scope-eligible case in a body publishes its counts and suppresses
  its yields, rates, and gate, naming the reason — a suppressed metric
  never renders as a number. The v30 closure pass ratified the granularity
  this suite implements: a scope-eligible case is every labelled case in
  the body, clean cases included (which is why T17's clean case had to be
  `not_applicable` for suppression to apply). The auto-added all-`not_applicable` promoted
  rows (T01–T04, T06–T08, T13–T16) and T15/T16's preserving rows are
  suppressed below; T05/T09/T10's promoted rows carry real promoted traces
  and publish numerically. T17 pins whole-body suppression on a multi-case
  body and T18 pins that a mixed body is NOT suppressed, its
  `not_applicable` cases contributing misses per §7.2/§7.4.

*(Metric ids contain literal `|` separators; in the tables below they are
escaped as `\\|` so markdown renderers keep the columns intact.)*
"""


def _fmt_value(mv) -> str:
    if mv.value is None:
        return "None (denominator 0)"
    return f"{mv.value:.4g}"


def _record_line(r) -> str:
    if r.valid:
        what = "silence" if r.finding is None else (
            f"finding({r.finding.feature}@{r.finding.affected_output_cohort}"
            f"{', secondary' if r.finding.is_secondary else ''})")
        return f"{r.strategy_id}@{r.cohort_id}: valid, {what}"
    return f"{r.strategy_id}@{r.cohort_id}: invalid({r.failure_reason.value if r.failure_reason else 'no reason recorded'})"


def render() -> str:
    lines = [HEADER]
    for fx in FIXTURES:
        lines.append(f"\n## {fx.fixture_id} — {fx.title}\n")
        lines.append(f"Prose basis: {fx.prose_basis}\n")
        for trace in fx.traces:
            prefix = gate_id_for(trace.detector_id, trace.promotion_status)
            recs = "; ".join(_record_line(r) for r in trace.records) or "(no records)"
            lines.append(
                f"- `{prefix}` — context {trace.run_context.value}, strategies "
                f"{list(trace.resolved_strategies)}, cohorts "
                f"{list(trace.selected_eligible_cohorts)}, inputs "
                f"{'available' if trace.required_inputs_available else 'MISSING'}, "
                f"terminal={'yes' if trace.terminal_decision_occurred else 'no'}")
            lines.append(f"  - records: {recs}")
        for lab in fx.case_labels:
            pairs = sorted(lab.leaking_pairs)
            lines.append(
                f"- labels `{lab.case_id}`: "
                + ("clean (no leaking pairs)" if lab.is_clean else f"leaking pairs {pairs}"))
        lines.append("\n**Expected state pair:**\n")
        for trace in fx.traces:
            prefix = gate_id_for(trace.detector_id, trace.promotion_status)
            state, outcome = resolve_state_pair(trace)
            reason = f"({state.reason.value})" if state.reason else ""
            lines.append(f"- `{prefix}` (`{trace.case_id}`) → "
                         f"`{state.kind.value}{reason}` × `{outcome.value}`")
        metrics = compute_runtime_metrics(fx.traces, fx.case_labels)
        lines.append("\n| metric | num | den | value |")
        lines.append("|---|---|---|---|")
        for mid in sorted(metrics):
            mv = metrics[mid]
            cell = mid.replace("|", "\\|")  # a raw | inside a cell breaks the table
            if isinstance(mv, SuppressedMetric):
                lines.append(f"| `{cell}` | — | — | **suppressed** — {mv.reason} |")
            else:
                lines.append(f"| `{cell}` | {mv.numerator} | {mv.denominator} | {_fmt_value(mv)} |")
        if fx.expected_gates or fx.expected_suppressed_gates:
            gates = apply_runtime_gates(metrics)
            for prefix, exp in fx.expected_gates.items():
                g = gates[prefix]
                lines.append(
                    f"\nGate `{prefix}`: experimental={g.experimental} "
                    f"(finding gate fired={g.finding_gate_fired}, completion gate "
                    f"fired={g.completion_gate_fired}; clean N={g.clean_n}, "
                    f"k={g.clean_findings}, completed={g.clean_completed})")
            for prefix in fx.expected_suppressed_gates:
                g = gates[prefix]
                assert isinstance(g, SuppressedGate)
                lines.append(f"\nGate `{prefix}`: **suppressed** — {g.reason}")
        if fx.notes:
            lines.append(f"\n> {fx.notes}")

    lines.append("\n## Assertion scenarios (PREREG §8.3)\n")
    for sc in ASSERTION_SCENARIOS:
        events = derive_evidence_events(sc.traces)
        gates = {
            p: GateResult(p, exp, exp, False, 1, 1 if exp else 0, 1)
            for p, exp in sc.experimental.items()}
        result = evaluate_runtime_assertions(events, gates)
        findings = derive_reported_findings(events, gates)
        lines.append(f"\n### {sc.fixture_id} — {sc.title}\n")
        lines.append(f"Prose basis: {sc.prose_basis}\n")
        lines.append(f"- gate status: " + ", ".join(
            f"`{p}` {'experimental' if e else 'non-experimental'}"
            for p, e in sc.experimental.items()))
        lines.append(f"- events: {len(events)}; reported findings: {len(findings)} "
                     f"(tier {findings[0].tier}, per-event gate status retained, "
                     "no single inferred boolean)")
        lines.append(f"- `assert_no_proven_leakage()` → "
                     f"{'passes' if result.no_proven_leakage_passed else 'FAILS'} "
                     f"({len(result.proven_triggering_events)} triggering event(s))")
        lines.append(f"\n> {sc.notes}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    OUT.write_text(render(), encoding="utf-8", newline="\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
