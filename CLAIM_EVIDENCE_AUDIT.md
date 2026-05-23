# Claim Evidence Audit

Audit date: 2026-05-22  
Primary draft: `Performance-Paper-PCA/Paper.tex`  
Evidence roots: `Performance/NOTES.md`, `Performance-Paper-PCA/PROJECT_LOG.md`, and CSV/log artifacts under `Performance/`.

## High-priority changes before editing the paper

1. **Do not claim FastGraph is faster than every backend at every dimension unless GGNN is excluded or explicitly recall-qualified.**
   - Paper lines 565-570 include GGNN among compared backends.
   - Paper lines 665-668 say FastGraph is faster than every backend at every dimension.
   - Evidence: `ggnn_mps50_calibration.csv` at `N=5M,k=40` has GGNN faster than FastGraph at d=2-6 in raw wall-clock:
     - d=2: GGNN 30.02 s vs FastGraph 89.02 s
     - d=3: GGNN 30.01 s vs FastGraph 102.97 s
     - d=4: GGNN 30.05 s vs FastGraph 132.49 s
     - d=5: GGNN 28.52 s vs FastGraph 97.97 s
     - d=6: GGNN 14.96 s vs FastGraph 29.29 s
   - Recommended fix: say FastGraph is fastest among exact backends and CAGRA-NN-Descent in the headline table; discuss GGNN separately as a low-recall approximate method.

2. **Synthetic section claim is false with the completed synthetic GPU baseline data.**
   - Paper lines 751-754 say FastGraph is the fastest GPU method across the synthetic dimensional range and the advantage widens above d=5.
   - Evidence: `synthetic_pca_benchmark.csv` + `synth_gpu_baselines.csv`, `N=1M,k=40`.
     - FastGraph beats FAISS/cuVS/CAGRA at d=2-6.
     - At d=7, cuVS BF is faster than FastGraph (speedup vs cuVS = 0.80x).
     - At d=8, FAISS and cuVS BF are faster than FastGraph (FAISS/FastGraph = 1.18x, cuVS/FastGraph = 0.61x).
     - At d=9-10, FAISS and cuVS BF are clearly faster than FastGraph.
   - Recommended fix: reframe synthetic as distribution-sensitive: PCA-FGC dominates low d and still beats CAGRA-NN-Descent, but brute-force exact backends overtake it at high-d isotropic Gaussian.

3. **Ablation table is stale.**
   - Paper lines 844-848 report older values.
   - Evidence: `ablation_max_bin_dims.csv` medians for `d=8,N=5M,k_nn=40`:
     - k=2: axis 154.79 s, PCA 8.33 s, speedup 18.57x
     - k=3: axis 148.24 s, PCA 5.52 s, speedup 26.87x
     - k=4: axis 204.19 s, PCA 5.90 s, speedup 34.60x
     - k=5: axis 129.45 s, PCA 15.78 s, speedup 8.21x
     - k=6: axis 71.86 s, PCA 33.31 s, speedup 2.16x
   - Recommended fix: update table and macro values. Note that headline `\fgcPCADeight=7.2 s` comes from the full headline sweep, while the ablation optimum at k=3 is 5.52 s; explain or reconcile this benchmark-context difference.

4. **Several figures referenced by `Paper.tex` are missing from `media/`.**
   - Missing references:
     - `gpu_fgc_speedup_d8_gpu.png`
     - `synth_dimensional_scaling_1M_k40_gpu.png`
     - `synth_speedup_d3_gpu.png`
     - `synth_speedup_d8_gpu.png`
     - `clover_headtohead_d3.png`
   - Existing likely older/similar names:
     - `synthetic_fgc_dimensional_scaling_1M_k40_all_algorithms.png`
     - `synthetic_fgc_speedup_d3_all_algorithms.png`
     - `synthetic_fgc_speedup_d5_all_algorithms.png`
   - Recommended fix: regenerate the new plots, or point the draft back to existing filenames and update captions.

5. **There is a broken cross-reference.**
   - Paper line 872 references `Section~\ref{sec:related-work}`.
   - The Related Work section currently has no `\label{sec:related-work}`.
   - Recommended fix: add `\label{sec:related-work}` immediately after `\section{Related Work}`.

6. **The PCA-paper bibliography is missing citation entries used by the draft.**
   - Missing from `Performance-Paper-PCA/references.bib`: `bhattacharya2022gnn`, `choma2020track`, `dashti2013efficient`, `feydy2020fast`, `ju2021performance`, `komarov2014fast`, `qasim2021multiparticle`, `qu2020particlenet`, `wang2019dynamic`, `wang2021large`.
   - These entries exist in the older `Performance/references.bib`; copy or merge them before compiling.

7. **CLOVER data should be included, but the conclusion/title-level story needs to avoid overclaiming state of the art.**
   - Evidence confirms paper table values from `pca_fgc_clover_headtohead.csv` and `clover_headtohead.csv`.
   - CLOVER hubs is much faster than FastGraph on d=3 HGCAL: 1.62 s vs 169 s at 5M.
   - FastGraph wins on uniform d=3: 0.246 s vs 1.83 s at 5M.
   - Recommended fix: keep the section, but avoid “state-of-the-art for exact GPU kNN in d=4-10” unless a literature claim can be defended beyond implementation availability.

## Substantiated headline claims

### HGCAL headline speedups at `N=5M,k=40`

Evidence sources:
- FastGraph: `gpu_fgc_pca_performance.csv`
- FAISS: `faiss_mps50_calibration.csv`
- cuVS BF: `cuvs_bf_mps50_calibration.csv`
- CAGRA-NN-Descent: `cagra_nn_descent.csv`

Median-derived speedups match the current headline table:

| d | FGC time | vs FAISS | vs cuVS BF | vs CAGRA-nnd |
|---|----------|----------|------------|--------------|
| 2 | 89.02 s | 3.42x | 1.65x | 1.51x |
| 3 | 102.97 s | 2.96x | 1.43x | 1.28x |
| 4 | 132.49 s | 2.30x | 1.12x | 1.01x |
| 5 | 97.97 s | 3.09x | 1.48x | 1.40x |
| 6 | 29.29 s | 10.51x | 4.92x | 4.52x |
| 7 | 8.70 s | 35.23x | 16.77x | 14.82x |
| 8 | 7.24 s | 42.46x | 20.15x | 18.03x |
| 9 | 9.45 s | 32.68x | 15.60x | 14.36x |
| 10 | 10.36 s | 29.83x | 14.31x | 13.17x |

Geomeans:
- FAISS: 10.11x
- cuVS BF: 4.84x
- CAGRA-NN-Descent: 4.40x

### Recall/exactness measurement

Evidence sources:
- `recall_dist_fgc.csv`
- `recall_dist_cuvs.csv`
- `recall_dist_ggnn.csv`
- `NOTES.md` recall-distance discussion

Supported:
- FastGraph recall_dist minimum is 1.0 across 66 rows, dimensions 2-10, max N=500k.
- cuVS/CAGRA at `itopk_size=512`: mean recall_dist 0.732, representative d=3,N=500k,k=40 recall 0.818.
- GGNN at `tau_query=0.8`: mean recall_dist 0.666, representative d=3,N=500k,k=40 recall 0.410.

Needs qualification:
- The paper says neither approximate method reaches 99% at `N >= 500k`; verify from all rows before leaving this as absolute. The summary calculation above only verified the highest-quality rows currently used.
- The claim that tuning approximate methods above FastGraph eliminates their speed advantage is only clearly tied to CAGRA headline data. GGNN needs either a matched-recall table or softer wording.

### CAGRA failure/fix story

Evidence sources:
- `PROJECT_LOG.md`, “CAGRA failure investigation”
- `cagra_nn_descent.csv`
- log files under `Performance/logs/`

Supported:
- Default IVF-PQ path fails at d>=5 on HGCAL.
- NN-Descent build succeeds across d=2-10.
- NN-Descent is the correct canonical CAGRA comparison for a full sweep.

Needs care:
- The proposed root cause (“heterogeneous scale causes PQ codebook collapse”) is a strong inference from the RAFT error and self-included ratio, not directly proven by a normalization ablation. Present as diagnosis/evidence, not as an experimentally isolated mechanism.

## Claims needing more evidence or softer wording

1. **“PCA estimation contributes negligibly”** (method line around Phase 1).
   - Need timing breakdown from profiler/logs or soften to “small in the benchmarked regimes.”

2. **“construction cost frequently dominates model wall-clock once latent dimensionality is anything other than two or three.”**
   - Need model-level profiling evidence or cite prior profiling; otherwise soften to “can dominate.”

3. **“HGCAL neighbors near kth cut are structurally informative” / “approximate backend introduces systematic into training/inference.”**
   - Plausible, but needs citation or a small model-quality argument. No local evidence found.

4. **“Data distribution no longer drives the speedup.”**
   - Current Clover and synthetic results show distribution still matters strongly. Recommended rewrite: PCA reduces raw feature-scale sensitivity but does not make performance distribution-independent.

5. **“FastGraph compiled from public release” and README reproduction instructions exist.**
   - Data/code statement should be verified against the public repo state before submission; local code appears to include dev/PCA changes that may not be public yet.

## Missing additions worth considering

1. **Add a small GGNN row or footnote in the headline section.**
   - Since setup includes GGNN, explain why it is excluded from Table 1: raw-fast at low d but low recall / approximate. Otherwise reviewers will ask.

2. **Add a short “completed Clover comparison” paragraph to Related Work or limitations.**
   - Clover is now run and should be used as a strength: FastGraph does not win d=3 HGCAL, but Clover cannot address d>=4 latent spaces.

3. **Add a synthetic-results caveat.**
   - The synthetic high-d reversal is scientifically useful: HGCAL heterogeneity is where PCA binning pays off most; isotropic Gaussian at high d favors brute force.

4. **Add a normalization/PQ ablation only if time allows.**
   - To fully substantiate the CAGRA root-cause claim, run CAGRA IVF-PQ on normalized HGCAL features and report whether failures disappear.

5. **Add a model-level motivation citation or measurement.**
   - If the paper leans on dynamic GNN training critical-path claims, include either prior work or a small GravNet profiling table.

## Mechanical checks

- `TBD` macros remain at lines 102-105 for synthetic speedups. They are not currently printed directly except in the synthetic prose. Remove or patch after final synthetic narrative.
- Figure files listed above are missing and will break LaTeX unless generated.
- Missing `sec:related-work` label will create an undefined reference.
- The current draft uses `---` in prose; that is fine for LaTeX but should be kept consistent.
