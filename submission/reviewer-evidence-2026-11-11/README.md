# November 11 reviewer-evidence draft

This packet supports the revised author-review manuscript. It is not a
journal submission or a new immutable experimental release. Historical
headline figures, release tags, author order and submission archives remain
unchanged.

## New manuscript evidence

- Experimental setup distinguishes three within-input timing repetitions
  from independent data seeds and from the historical campaign.
- Controlled covariance/normalization results and Table 2 add three-seed
  paired speedups with explicitly exploratory confidence intervals.
- Memory includes independent-process NVML sampled peaks/baselines.
- Numerical reporting extends full FP64 checks through 32,768 detector-prefix
  points and sampled checks at one million; it distinguishes structural
  success from numerical reference agreement for external backends.
- Candidate counters and gradient diagnostics support a bounded mechanism
  and integration claim; limitations retain missing real event/model evidence.

## Source identities

FastGraph library: `76a869cc8758a8a846b18e93934e2b6078d83279`.

| Local return | Frozen harness | Plan SHA-256 | Scope |
|---|---|---|---|
| a100-complement-20261110 | 8265bfd | c693d97f6e75875001a6e41a016c3ae956e26c46b4154e57c32f6438622f808b | 41 synthetic/control cases, 421 successful bundles |
| a100-reverse-64808 | b0ba36f | a03b48a7ed7b528b857c471765f96551a1f8414ee3a97d7e57a8785772e09a57 | 63 extension cases; original return 654 successful, one FAISS failure and 13 missing |
| a100-faiss-repair-64820 | b72fa54 | ee6135bac6fcb7b645f707a7e6a0068d215f76296d5e9daf5e8e9859e53b18f1 | 17 cases / 152 successful bundles; every affected backend repeated, plus numerical gates |

`paired-exact-comparisons.csv` contains same-plan/input/GPU paired median
ratios; `seed-uncertainty.csv` and `UNCERTAINTY.md` document the across-seed
analysis after collapsing repeated controls. `RESULTS.md` records the
original combined coverage, numerical results and limitations. None of
these exports contains raw detector coordinates, event IDs, model weights
or owner notes. Raw inputs remain subject to CMS access conditions.

The repaired return is analyzed separately because its backend harness
changed. Successful targeted repair does not rewrite the original plan's
coverage or add an independent seed. Its final reconciliation is recorded
in `reconciliation.json`: all 14 original failed/missing tasks now have
successful repaired evidence with matching task/input/hardware identities.
The old return retains its failure and missing counts. GPU64819 completed
in 10m43s; export/analysis CPU64820 completed in 16s. No GPU jobs remain
queued. `repair-COVERAGE.md` and `repair-RESULTS.md` describe the separate return.

## Reviewer coverage still incomplete

Read `EVIDENCE_AUDIT.md`. Real event correspondence/feature definitions,
trained learned-coordinate inputs, actual model throughput and H100 runtime
are still absent. The original numbered reports and Reviewer 18 attachment
are needed for a complete point-by-point response. Neither software tests
nor repeated synthetic timings close those evidence gaps.

## Rebuild

Run `latexmk -pdf -pdflatex='pdflatex -no-shell-escape %O %S' Paper.tex`
from the manuscript repository root. Existing source bundles remain
historical snapshots; use the current root source for this draft.
`FastGraph-reviewer-evidence-source.zip` contains the current 11-file source
bundle and passes archive integrity/fresh-build checks. The build produces
22 pages with matching extracted PDF text, embedded fonts, resolved references,
no overfull boxes and three existing bibliography underfull diagnostics.
The contact sheet, new covariance/CI table and availability page were
visually inspected. `validate_table.py` independently recomputes all four
table rows from the paired CSV and confirms three timing repetitions in
all 1,395 recorded configurations. `timing-repeatability.csv` contains the
descriptive per-configuration variability; `UNCERTAINTY.md` explains why
that is distinct from confidence across independent inputs.
