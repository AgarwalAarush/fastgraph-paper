# FastGraph: PCA-Subspace Exact GPU kNN

This is the manuscript repository for the FastGraph paper, with an arXiv
preprint layout and an archived *Array* submission. It contains the source,
compiled PDF, and the single authoritative guide to reproducing every figure.

## Release Entry Point

Use the immutable `pca-fgc-paper-v1.3.4` tag for the experimental artifacts. The current manuscript includes the September 29, 2026 Array editorial corrections; that older tag preserves the preceding manuscript.
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

## arXiv Upload

The `arxiv-preprint-v1.0.0` tag preserves the preprint with the updated
typography, checked float placement, and lowercase author emails.

Use [submission/arxiv/FastGraph-arXiv-source.zip](submission/arxiv/FastGraph-arXiv-source.zip)
with `Paper.tex` as the main file and pdfLaTeX / TeX Live 2023. The bundle
contains the current manuscript, its compiled BibTeX bibliography, the `.bib`
source, and only the eight referenced PDF figures. Review arXiv's generated
PDF before completing submission. See [the bundle notes](submission/arxiv/README.md).
