#!/usr/bin/env python3
"""DELTA R65/K3 - record the description-staleness lesson as H-L18."""
import pathlib

REPO = pathlib.Path("C:/Users/ttbea/OneDrive/Desktop/MBO_2025(4mon)+2026-01")
h = REPO / "HISTORY.md"
L = h.read_text(encoding="utf-8").split("\n")
i = next(k for k, l in enumerate(L) if l.startswith("17. *(21 Aug 2026)* One tool produced three separate failures"))
assert L[i + 1].strip() == "", "lesson 17 does not end where expected"

LESSON = ('18. *(21 Aug 2026)* **A registered redesign changes what a criterion MEANS, and every passage '
          'that DESCRIBES it is stale from that moment until somebody re-derives it.** The descriptions do '
          'not announce this. They go on reading fluently, in the register of settled fact, describing an '
          'object that no longer exists \u2014 which is why all three instances here surfaced months later and '
          'none surfaced by being noticed in passing. **Instance one: the declared map lagged Y1.** Y1 '
          'ruled that no fed column is MBO-fed; the map went on carrying 360 SCORED, strict-positive cells '
          'across six `mbo_*` classes, predicting REQUIRED findings that no unit could carry, under a '
          'clause declaring its three dispositions "mutually exclusive and exhaustive over the map". '
          '**Instance two: the declaration\'s artifact allocation lagged R9.** \u00a70.1 and \u00a70.2 were written '
          'when criterion 3 read "no runtime finding appears on `fixture_corrected`" \u2014 a silence test, '
          'answerable from any artifact that can be observed to produce nothing. R9 replaced silence with '
          'map-scoring, which made the criterion require a **column** and a **cell**; the allocation was '
          'never re-derived, and went on saying criteria 1\u20134 were "all statements about Artifact B" \u2014 an '
          'artifact the same section says stores **no feature columns**. Under that description criterion '
          '4\'s identity control had no `net_delta` to run over and was unevaluable, which is how far a '
          'stale description can travel without tripping anything. **Instance three: the \u00a76.2 line-459 '
          'marker lagged R11.** It read "ADDED NOT SUPERSEDED \u2014 criterion 1 stands byte-exact", true of the '
          'bytes and false of the requirement: R11 moved the denominator to a derived partition, and on 14 '
          'of 25 leaking-source columns the demand inverts from *absence is a miss* to *a finding fails the '
          'gate*. **The common shape: the amendment edits the RULE and leaves the DESCRIPTION, and a '
          'description is what a reader actually reads.** A byte-level diff shows nothing at any of the '
          'three sites, which is precisely why the check has to be semantic. **After any semantic '
          'amendment, sweep the descriptions** \u2014 every passage in every corpus that describes the amended '
          'object, judged against what the object now is, with a passage that merely RESTATES the old rule '
          'counted stale even where it contradicts nothing. And the sweep is done by somebody who did not '
          'draft the amendment, because the drafter reads the description and sees what they meant.')

L[i + 1:i + 1] = [LESSON]
h.write_text("\n".join(L), encoding="utf-8")
print("H-L18 recorded (%d lines)" % len(L))
