# Reproducibility Guide

## Release Identity

Check out `pca-fgc-paper-v1.3.4` in every repository. These tags identify the
exact library, benchmark, plotting, and CLOVER-fork revisions used for the
historical headline experiments. The current manuscript also incorporates
the September/October editorial revisions and the November 11 supplementary
reviewer study; the tag retains the earlier manuscript. Historical figure
artifacts remain unchanged. New supplementary measurements have separate
plan/harness identities and are not covered by the old experimental tags.

## Supplementary Reviewer Evidence

The author-review packet under `submission/reviewer-evidence-2026-11-11/`
records the new source plans and aggregate comparison/uncertainty tables.
The original campaigns used frozen harnesses `8265bfd` and `b0ba36f`;
the separate matched-case FAISS repair uses `b72fa54`, which also adds the
seed-uncertainty analysis and CPU regression tests. All use the same pinned
FastGraph library `76a869cc8758a8a846b18e93934e2b6078d83279` on A100.
The repair preserves prior successes/failures and repeats whole affected
cases; its rows are not silently pooled across changed harnesses.

Three timing repetitions per fixed input measure timing variability.
Three independent data seeds support the principal K=40 synthetic
comparisons. The exploratory confidence intervals use Student-t intervals
on paired seed log-speedups, not the timing repetitions as independent
datasets. One-input controls have no across-input CI. See the packet's
`UNCERTAINTY.md` for assumptions and scope.

## Recreate The Figures From Public Artifacts

1. Clone `fgc-performance` and enter `reproduction/`.
2. Verify `results/CHECKSUMS.sha256` with `sha256sum -c` from `results/`.
3. Run `python plots/make_paper_plots.py` to regenerate the figure set from
   the canonical CSVs.
4. Compare or copy the generated figures into this repository's `media/`, then
   build `Paper.tex` with `latexmk`.

This path does not require access to restricted CMS data.

## Re-run The HGCAL Campaign

Approved collaborators set `SHAREDDATA_DIR` to the CMS-restricted recHit
artifact, then run `prepare_matched_input_queues.sh` and
`submit_matched_input_campaign.sh` from `fgc-performance/reproduction/scripts/`.
The campaign is serialized at `--gres=mps:100`, uses the same preloaded
GPU-resident input for every backend, and writes into a fresh `run/` directory.

## Public Synthetic Reproduction

`fgc-performance/reproduction/synthetic/` contains the seeded synthetic
benchmark generators. It is the public, unrestricted path for exercising the
method without CMS data.

## Scope And Data Policy

Historical release plotting inputs, code, configurations, and checksums
are available through the release repositories. New evidence in this draft
has separate author-review status as documented in its packet. The
43 GiB HGCAL input remains restricted by CMS data access conditions and is
therefore neither published nor required to reproduce the checked-in figures.
`clover-knn` is a pinned third-party comparison fork, not a FastGraph product.
