# FastGraph: PCA-Subspace Exact GPU kNN

This is the manuscript repository for the FastGraph paper. The current
source and PDF contain the physics-facing rewrite with November 11, 2026
reviewer evidence: controlled covariance/feature scaling, explicit seed
uncertainty, numerical checks, and sampled peak memory. This is an author-review
draft, not a submitted or newly tagged release. The historical headline
figures and preprint typography are retained.
Historical *Array* and arXiv submission bundles remain archived separately.

Read [the new evidence packet](submission/reviewer-evidence-2026-11-11/README.md)
for source identities, replication limits, and reviewer requests still unmet.

## Current CPC Manuscript

Read [the revision package](submission/cpc-resubmission-2026-10-24/README.md)
for the manuscript, source bundle, editor-response draft, change log, and
author-confirmation flags. This is a proposed new CPC submission following
the September 20 desk decision. No journal submission has been made by this
editing pass; the separate Array consideration must be resolved by the authors.

## Release Entry Point

Use the immutable `pca-fgc-paper-v1.3.4` tag for the experimental artifacts.
The current manuscript includes the September 29 corrections and the October
24 CPC rewrite; the older tag preserves the preceding manuscript.
The earlier `v1.0.1` release remains intact as the original submission audit
record.

| Repository | Role |
|---|---|
| `AgarwalAarush/FastGraphCompute` | CUDA/PyTorch library and tests |
| `AgarwalAarush/fgc-performance` | Canonical results, scripts, and plotting |
| `AgarwalAarush/fastgraph-paper` | This manuscript, PDF, figures, and guide |
| `AgarwalAarush/clover-knn` | Pinned third-party d=3 comparison fork |

Read [REPRODUCIBILITY.md](REPRODUCIBILITY.md) before using the benchmark
artifacts. The restricted HGCAL source is not public; the exact result CSVs
and synthetic reproduction are public.

## Building The Paper

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error Paper.tex
```

`Paper.pdf` is the compiled release artifact. `media/` contains the figures
referenced by the manuscript.

## Archived arXiv Upload

The `arxiv-preprint-v1.0.0` tag preserves the preprint with the updated
typography, checked float placement, and lowercase author emails.

Use [submission/arxiv/FastGraph-arXiv-source.zip](submission/arxiv/FastGraph-arXiv-source.zip)
with `Paper.tex` as the main file and pdfLaTeX / TeX Live 2023. The bundle
contains the October 22 preprint, its compiled BibTeX bibliography, the `.bib`
source, and only the eight referenced PDF figures. Review arXiv's generated
PDF before completing submission. See [the bundle notes](submission/arxiv/README.md).
