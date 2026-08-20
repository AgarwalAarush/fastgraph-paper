# Reproducibility Guide

## Release Identity

Check out `pca-fgc-paper-v1.3.0` in every repository. These tags identify the
exact library, benchmark, plotting, manuscript, and CLOVER-fork revisions for
the clean public release.

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

All plotting inputs, code, configurations, and checksums are public. The
43 GiB HGCAL input remains restricted by CMS data access conditions and is
therefore neither published nor required to reproduce the checked-in figures.
`clover-knn` is a pinned third-party comparison fork, not a FastGraph product.
