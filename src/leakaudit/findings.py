"""A view over what a probe emitted, so a caller does not walk records. R201 P1.

WHY A VIEW AND NOT A RESULT OBJECT. A wrapper cannot disagree with what it
wraps; a copy can. Every parallel representation in this project's history
eventually disagreed with its source -- an emitter that kept one moved column and
dropped the rest, a line-pinned citation whose number contradicted its own
recorded reason, a manifest that had to be regenerated rather than hand-merged.
So this stores no derived state. `findings` is computed from the traces on every
access, `outcome` is computed by the registered reducer on every access, and
anything the traces do not carry is reached through a reference to the object
that does carry it, never extracted into a field here.

THE ACCESSOR QUALIFIES ITS OWN SILENCE, and that constraint applies here harder
than anywhere else, because this is what a user reads first. An empty result is
exactly the silence this tool exists to be careful about. It says which kind it
is, in the registered vocabulary:

    finding            something moved
    observed_silence   probes ran at cohorts and nothing moved
    none               no probe ran -- there is nothing to have found

`none` is NOT `observed_silence`. A probe that did not happen is not a probe that
found nothing, and a user acting on the second when the first is true is acting
on an absence they believe is evidence.

THE COMBINED OUTCOME IS A DISPLAY PROJECTION AND IS LABELLED ONE. The registered
outcome is per combination -- `PREREG.md` §6.6 keys it on (detector, promotion
status, case) -- and each combination's own outcome stays available at
`per_combination`. The single value here is for a human reading one line, and no
gate arithmetic is computed from it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from protocol.runtime_reference import (
    CombinationTrace, EvidenceOutcome, derive_evidence_events,
    resolve_evidence_outcome)


@dataclass(frozen=True)
class Finding:
    """One moved feature, derived on access. Never stored.

    ONE PER REGISTERED UNIT, NOT ONE PER RECORD. `PREREG.md` §7.2: within a
    combination, probe cohorts, strategies and repeated runs are corroborating
    evidence, not additional events -- a pair found by three probes and two
    strategies is one event, one true positive. Deriving from records instead
    printed the same finding once per strategy, which is a count of the
    schedule rather than of what was found. Caught by running the command, not
    by reading the code.
    """
    feature: str
    affected_output_cohort: str
    detector: str
    promotion_status: str
    is_secondary: bool
    probe_cohorts: tuple = ()
    strategies: tuple = ()

    def __str__(self) -> str:
        tail = " (secondary)" if self.is_secondary else ""
        where = ", ".join(self.probe_cohorts) or "?"
        how = ("corroborated by %s" % ", ".join(self.strategies)
               if len(self.strategies) > 1
               else "under %s" % (self.strategies[0] if self.strategies else "?"))
        return "%s moved when %s was perturbed [%s/%s, %s]%s" % (
            self.feature, where, self.detector, self.promotion_status, how, tail)


class AuditResult:
    """A view over one probe's traces. Holds references; derives everything else.

    `source` is the object the probe returned, kept BY REFERENCE so that facts
    it carries and the traces do not -- what was outside the probe's domain, and
    which supplied frames the model did not describe -- are read from it rather
    than copied here. A copy is the thing that drifts.
    """

    def __init__(self, traces: Iterable[CombinationTrace], source=None,
                 checks: Iterable = ()) -> None:
        self._traces = tuple(traces)
        if not self._traces:
            raise ValueError(
                "an AuditResult over no traces could report only silence, and "
                "could not say which kind it was")
        self._source = source
        # Held by reference like `source`: these are results the checks produced,
        # not a second derivation of them.
        self._checks = tuple(checks)

    @property
    def checks(self) -> tuple:
        """The no-model checks, each carrying whether it looked."""
        return self._checks

    # -- the traces, unmodified -------------------------------------------
    @property
    def traces(self) -> tuple[CombinationTrace, ...]:
        return self._traces

    @property
    def source(self):
        return self._source

    # -- derived on every access ------------------------------------------
    @property
    def findings(self) -> list[Finding]:
        """Derived by the FROZEN REDUCER on every access, never stored.

        `derive_evidence_events` is the registered deduplication: one event per
        combination per (feature, affected cohort), with probes and strategies
        as corroboration. Using it here means this view counts what the
        registration counts rather than a second thing that resembles it.
        """
        return [
            Finding(feature=e.feature,
                    affected_output_cohort=e.affected_output_cohort,
                    detector=e.detector_id,
                    promotion_status=e.promotion_status.value,
                    is_secondary=e.is_secondary,
                    probe_cohorts=tuple(sorted(e.probe_cohorts)),
                    strategies=tuple(sorted(e.strategies)))
            for e in derive_evidence_events(self._traces)]

    @property
    def per_combination(self) -> dict[str, str]:
        """The REGISTERED outcome, per combination, by the frozen reducer."""
        return {t.promotion_status.value: resolve_evidence_outcome(t).value
                for t in self._traces}

    @property
    def outcome(self) -> str:
        """A DISPLAY projection over the per-combination outcomes."""
        values = [resolve_evidence_outcome(t) for t in self._traces]
        if any(v is EvidenceOutcome.FINDING for v in values):
            return EvidenceOutcome.FINDING.value
        if any(v is EvidenceOutcome.OBSERVED_SILENCE for v in values):
            return EvidenceOutcome.OBSERVED_SILENCE.value
        return EvidenceOutcome.NONE.value

    @property
    def cohorts_probed(self) -> tuple[str, ...]:
        seen: list[str] = []
        for t in self._traces:
            for c in t.selected_eligible_cohorts:
                if c not in seen:
                    seen.append(c)
        return tuple(seen)

    @property
    def unprobed_frames(self) -> tuple[str, ...]:
        """Frames the caller supplied that the model does not describe.

        Read from the source by reference. A probe that has no such notion
        reports none, which is a different statement from reporting an empty
        list after checking -- and the difference is stated rather than left to
        the reader.
        """
        return tuple(getattr(self._source, "unmodelled_frames", ()) or ())

    @property
    def notes(self) -> tuple[str, ...]:
        """What the probe said about the run, read from the source by reference.

        THESE WERE INVISIBLE TO EVERY CLI USER UNTIL R208 §3, and the omission
        was found by walking the stranger path rather than by any test. The
        probe appends notes for things a reader has to know -- that a
        non-boundary key was floored, that a declared frame was absent and so
        nothing in it was corrupted, that a column with no declared mode took
        the frame's rule -- and `explain()` rendered `unprobed_frames`,
        `domain` and the check results while never rendering these. So the
        reports existed in the library and reached nobody running the command.

        A report nothing prints is not a report. It is the shape this tool
        exists to detect, in the tool.
        """
        return tuple(getattr(self._source, "notes", ()) or ())

    @property
    def domain(self) -> str:
        """What the probe did and did not look at, in its own words."""
        return str(getattr(self._source, "domain", "") or "")

    # -- the part that matters most ---------------------------------------
    def explain(self) -> str:
        """What this result is, and for an empty one, WHICH KIND of empty."""
        n = len(self.findings)
        if n:
            feats = sorted({f.feature for f in self.findings})
            head = "%d finding(s) over %d feature(s): %s" % (
                n, len(feats), ", ".join(feats))
        elif self.outcome == EvidenceOutcome.OBSERVED_SILENCE.value:
            head = ("OBSERVED SILENCE: %d cohort(s) were probed and nothing "
                    "moved. This is evidence." % len(self.cohorts_probed))
        else:
            head = ("NONE: no probe ran, so there is nothing to have found. "
                    "THIS IS NOT EVIDENCE OF ABSENCE -- it is the absence of "
                    "evidence, and it is reported separately for that reason.")
        parts = [head]
        if self.unprobed_frames:
            parts.append(
                "NOT PROBED: %s -- supplied and not described by the model, so "
                "nothing downstream of %s could have moved whatever the pipeline "
                "does. Any silence about %s is `none`, not `observed_silence`."
                % (", ".join(self.unprobed_frames),
                   "them" if len(self.unprobed_frames) > 1 else "it",
                   "them" if len(self.unprobed_frames) > 1 else "it"))
        if self.domain:
            parts.append("DOMAIN: %s" % self.domain)
        # The unprobed-frames fact is rendered above from the structured field,
        # and the probe ALSO states it as a note in its own words. Printing both
        # says the same thing twice in one screen, which teaches the reader that
        # this section repeats itself and can be skimmed -- the opposite of what
        # it is for. Dropped by subject, not by string equality: the two
        # wordings differ, so a substring test silently kept both.
        notes = [n for n in self.notes if not n.startswith("NOT PROBED:")]
        if notes:
            parts.append("ABOUT THIS RUN:\n%s"
                         % "\n".join("  - %s" % n for n in notes))
        if self._checks:
            ran = sum(1 for c in self._checks if c.looked)
            hit = sum(1 for c in self._checks if c.outcome == "finding")
            parts.append(
                "CHECKS: %d of %d ran, %d with findings. The %d that did not run "
                "are reported as not-looked rather than counted as clean."
                % (ran, len(self._checks), hit, len(self._checks) - ran))
        return "\n".join(parts)

    def __str__(self) -> str:
        """A projection. It reads the same traces and holds nothing."""
        lines = ["leakaudit: %s" % self.outcome,
                 "  per combination: %s" % ", ".join(
                     "%s=%s" % kv for kv in sorted(self.per_combination.items()))]
        for f in self.findings:
            lines.append("  - %s" % f)
        lines.append("")
        lines.append(self.explain())
        return "\n".join(lines)

    def __repr__(self) -> str:
        return "AuditResult(outcome=%r, findings=%d, cohorts=%d)" % (
            self.outcome, len(self.findings), len(self.cohorts_probed))
