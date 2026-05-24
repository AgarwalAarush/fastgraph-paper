# FastGraph: PCA-Subspace Binned Exact GPU kNN

ICML submission paper repository. Contains the paper source
(`Paper.tex`), bibliography (`references.bib`), figures (`media/`),
the compiled PDF (`Paper.pdf`), and an editing-audit trail
(`PAPER_CHANGES.md`, `PROJECT_LOG.md`, `CLAIM_EVIDENCE_AUDIT.md`,
`REWRITE_NOTES.md`).

## What the paper claims

FastGraph is the **fastest exact GPU $k$-nearest-neighbor method** in
the $d \in [4, 10]$ regime on detector data, the deployment regime for
HEP-GNN dynamic graph layers in HGCAL reconstruction. Headline
geomean speedups over the next-best exact GPU baseline (cuVS BF):
**$\sim 4.8\times$**; over FAISS-GPU: $\sim 10\times$; over
CAGRA-nn-descent: $\sim 4.4\times$.

Three honest caveats are documented throughout, not buried:

1. **PCA short-circuit at $d \leq k_{\mathrm{bin}}$**: the PCA projection
   is dead code at $d \leq 3$ with default settings; the $d{=}2{-}4$ HGCAL
   wins inherit from the legacy cell-list machinery.
2. **CLOVER beats FastGraph by $\sim 100\times$ at $d{=}3$ on HGCAL**.
   CLOVER is hardware-locked to $D{=}3$, so doesn't threaten the
   $d{=}4{-}10$ regime that FastGraph targets.
3. **PCA-FGC degrades on isotropic data**: crossover at $d{=}7$ on
   isotropic Gaussian; cuVS BF wins from $d{=}7$ onward. The HGCAL
   wins at $d{=}6{-}10$ are an anisotropic-data result, not a generic
   cell-list miracle.

## Building the paper

```bash
latexmk -pdf -interaction=nonstopmode Paper.tex
```

Requires TeX Live 2023+ with the `elsarticle` class. The build
artifacts (`*.aux`, `*.bbl`, `*.blg`, `*.log`, etc.) are gitignored;
`Paper.pdf` is committed as a release artifact.

## Companion repositories

Reproducibility is split across four repositories. They migrated to
owned remotes on 2026-05-23 (see `PROJECT_LOG.md`).

| Repository | Purpose |
|---|---|
| [`AgarwalAarush/FastGraphCompute`](https://github.com/AgarwalAarush/FastGraphCompute) | FastGraph library source (fork of [`jkiesele/FastGraphCompute`](https://github.com/jkiesele/FastGraphCompute)). Headline numbers were collected at branch `paper-release`, tag `v1.0-paper`, commit `011d295`, built against the CUDA 12.1 toolchain. |
| [`AgarwalAarush/fgc-performance`](https://github.com/AgarwalAarush/fgc-performance) | Benchmark harness, queue files, generator scripts, SLURM wrappers, and every per-backend timing CSV used to draw the figures. |
| [`AgarwalAarush/FastGraph-Plotting`](https://github.com/AgarwalAarush/FastGraph-Plotting) | Plot generation. `make_paper_plots_v4.py` produces the 13 figures `Paper.tex` references from the canonical CSVs. |
| [`AgarwalAarush/clover-knn`](https://github.com/AgarwalAarush/clover-knn) | CLOVER fork with the CMU Falcon A100 build, $k{=}40$ alignment, and the mesh-path runner used in §5.6 (Figure 9). Fork of [`ampslab/clover-knn`](https://github.com/ampslab/clover-knn). |

## Reproducing the numbers

1. Install FastGraph from the `v1.0-paper` tag of the FastGraphCompute
   fork into a fresh conda env (CUDA 12.1 toolchain).
2. Clone `fgc-performance` and place the HGCAL recHits feature file
   ($\sim$43 GB; internal to CMS; external parties contact the
   corresponding author).
3. Run `bash run_all.sh` (or `sbatch run_all_slurm.sh` on SLURM). Each
   backend writes one row per `(d, N, k)` cell to its CSV.
4. Clone `FastGraph-Plotting`, run
   `python make_paper_plots_v4.py`, copy the outputs to `media/`,
   recompile `Paper.tex`.

The synthetic-data plots use seeded `numpy.random.default_rng(SEED)`
draws — fully reproducible without HGCAL access; see
`synthetic_pca_benchmark_binA.py` in `fgc-performance`.

## Status and pending work

Living edit list at `PAPER_CHANGES.md`. Most items through `v4.2` are
landed. Two pending items (your call to add):

- **O38**: systematic-study text in Limitations citing
  `zugner2018adversarial` and `klicpera2019diffusion` to motivate
  exact-kNN deployment in GNN inference.
- **O39**: brief future-direction mention of hybrid PCA-LBVH /
  PCA-BVH for handling spatial-occupancy skew.

## Layout summary

```
.
├── Paper.tex                    # main source, ~1400 lines
├── Paper.pdf                    # compiled release artifact (21 pp.)
├── references.bib               # bibliography
├── media/                       # 13 figures used by Paper.tex
│   ├── gpu_fgc_dimensional_scaling_5M_k40_all_algorithms.png
│   ├── gpu_fgc_k_comparison_1M_d2-10_all_algorithms.png
│   ├── gpu_fgc_speedup_d{3,8}_*.png
│   ├── synth_dimensional_scaling_1M_k40_gpu.png
│   ├── synth_speedup_d{3,8}_gpu.png
│   ├── clover_headtohead_d3.png
│   ├── memory_footprint.png
│   └── recall_*.png             # 4 recall plots
├── PAPER_CHANGES.md             # living edit list, items grouped by section
├── PROJECT_LOG.md               # append-only decision audit log
├── CLAIM_EVIDENCE_AUDIT.md      # Codex-agent review that drove v3 rewrites
├── REWRITE_NOTES.md             # notes from the v1 PCA-subspace rewrite
└── lbvh_research_report.md      # background literature pulled during write-up
```
