# FastGraph: PCA-Subspace Exact GPU kNN

This is the manuscript repository for the FastGraph paper, prepared for
submission to *Computer Physics Communications*. It contains the source,
compiled PDF, and the single authoritative guide to reproducing every figure.

## Release Entry Point

Use the immutable `pca-fgc-paper-v1.1.0` tag across the repositories below.
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
