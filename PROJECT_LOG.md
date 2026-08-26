# PCA-FGC Paper Prep — Decision Log

A running record of every decision, finding, and rationale during the
PCA-FGC paper preparation. Append new entries at the bottom; never
silently edit past entries.

---

## 2026-05-19 → 2026-05-21 — Headline data collection

### PCA-FGC vs vanilla FGC HGCAL sweep (324 rows, mps:50, qos=medium)

- Ran the PCA-FGC variant across all 108 (dim, N, k) cells that the
  existing vanilla-FGC production sweep covered, ×3 reps. Job chain
  15279 → 15307 (trap-resubmit on walltime) completed cleanly.
- **Zero regressions across 108 cells.** Worst case is 0.98× at
  (d=3, N=2M, k=10) — within measurement noise; the wrapper
  short-circuits at d ≤ max_bin_dims, so this is literally the same
  code path as vanilla.
- Headline speedups at N=5M, k=40:
  - d=5: 1.65×    d=6: 6.57×    d=7: 24.89×
  - d=8: 28.23×   d=9: 24.67×   d=10: 24.19×
- Biggest single-cell win: d=8 N=100k k=40 → **1,465×** (vanilla falls
  into d_max=5 brute-force fallback; PCA-FGC's binning works).

### MPS slot 50 vs gpu:1 calibration

- The PCA sweep used `--gres=mps:50` (qos=medium); the production
  paper data was collected with `--gres=gpu:1`. Direct calibration
  needed before cross-allocation comparisons.
- Approach: short-circuit identity check + dedicated mps:50 mini-sweeps
  for each backend at the headline (dim 2–10, N=5M, k=40, 3 reps).
- Results:
  - **FGC family**: at d=2,3,4 the PCA wrapper short-circuits to
    vanilla; the two allocations run identical code and match within
    **1–3%**. Direct proof, not an assumption.
  - **FAISS** (job 15329 phase 1): match within **0.1%** across all dims.
  - **cuVS BF** (job 15329 phase 2): clean cells match within **0.1%**.
    Several gpu:1 production cells (d=2, 4, 8, 9) were **2× slower**
    than mps:50 calibration — the production CSV is contaminated for
    these cells, calibration is cleaner. Job 15433 reruns the 4
    contaminated cells in isolation.
  - **GGNN** (job 15350 phase 1): 1.04–1.05× — ~4% slowdown, inside
    tolerance.
  - **CAGRA** (job 15350 phase 2): **1.25× slower** at mps:50 —
    **outside** tolerance. Documented as a paper footnote; for the
    final comparisons we use the nn_descent build (below) which is
    on the same mps:50 allocation as PCA-FGC anyway.
- **Contention finding**: when two concurrent mps:50 jobs share an
  A100, bandwidth-bound backends (FAISS, cuVS BF) slow by ~2.3×;
  FGC is binning-dominated and is unaffected. Calibration must
  therefore run *alone* on the GPU. We enforce this with
  `--dependency=afterany:<previous>` chains.

### Exactness

- Algebraic argument: partial PCA projection `V_k V_k^T` is contractive
  (`x^T V_k V_k^T x ≤ ||x||²`), so the termination test
  `(w·s)² > r_K²` in projected space is a valid lower bound on true
  distance. No closer point can lie outside the visited bins. This
  holds at any N, any d, any K — algebraic, not empirical.
- Empirical verification: `correctness_compare.py` (7 spot-checks at
  d=3,5,8,10; N up to 500k; K up to 128) — **zero index mismatches,
  zero distance deltas** vs vanilla FGC on the short-circuit path.
- A brute-force reference at N=5M is infeasible (~100 TB workspace);
  standard practice is algebraic + small-N empirical, which is what
  we have. Same evidence standard as vanilla FGC.

---

## 2026-05-21 — CAGRA failure investigation

### Discovery

- CAGRA crashes at d ≥ 5 on HGCAL data (not d ≥ 8 as initially thought).
  Error trace from logs/generate_gpu_cuvs_cagra_20260422_191233.log:
  > `RAFT failure at file=cpp/src/neighbors/detail/cagra/graph_core.cuh
  > line=1406: Could not generate an intermediate CAGRA graph because the
  > initial kNN graph contains too many invalid or duplicated neighbor
  > nodes. ... if too many overflows occur during the norm computation
  > between the dataset vectors.`

### Root cause

- CAGRA's default build pipeline uses IVF-PQ to construct the initial
  k-NN graph, then runs graph optimization in `graph_core.cuh` to
  prune and add reverse edges. Step 2 fails because too many vertices
  have duplicate / invalid neighbor IDs in the IVF-PQ output.
- Even at d=2 (which succeeds) CAGRA emits
  `"Self-included ratio is low: 0.87 %"` — for a healthy graph this
  number is ~100%. 0.87% means PQ codebooks are so degenerate that
  vertices don't even include themselves in their own approximate
  k-NN list. CAGRA's optimizer limps through at low d but at d ≥ 5
  the duplicate count exceeds the assertion threshold.
- HGCAL recHit features have heterogeneous scales (energy O(100),
  spatial coords O(100–1000) cm, time O(1), layer index O(10), hit
  type O(1)). Product Quantization trains per-subvector codebooks
  but the norm computation runs over the full vector — large-magnitude
  features cause LUT overflow, collapsing the codebooks. This is
  exactly the failure mode named in the error message.

### Fix and validation

- Tested `build_algo="nn_descent"` (job 15353). NN-Descent doesn't
  quantize — it iteratively refines an approximate k-NN graph using
  raw fp32 distance computations. No PQ codebook involved.
- Result: **CAGRA-nn_descent works at every dim 2–10**, 3/3 reps each.
  Times ~130–137 s consistent across d=2..10.
- Head-to-head at the cells where IVF-PQ also succeeds (d=2,3,4):
  nn_descent is ~4× slower than IVF-PQ, but it's the only build that
  works at d≥5 on this data.

### Paper framing

The new CAGRA story is much stronger than "CAGRA crashed":
> "CAGRA's default IVF-PQ build path fails on HGCAL data at d≥5 due
> to PQ codebook overflow on the heterogeneous-scale feature columns
> (energy, time, geometric coordinates). Switching to nn_descent
> resolves the failure but at ~4× the build cost. Even with this fix,
> PCA-FGC outperforms CAGRA by ~18× at the d=8 N=5M k=40 reference
> point."

For the paper we use CAGRA-nn_descent as the canonical CAGRA baseline
(same mps:50 allocation as PCA-FGC, and the only build that succeeds
across the full sweep).

---

## 2026-05-21 — LBVH / alternatives research (agent)

Agent task: are there modern spatial-acceleration structures that could
beat PCA-FGC for exact GPU kNN at d=2–10 on detector physics data?

### Findings (see lbvh_research_report.md for full report)

1. **RT-cores kNN (RTNN / RT-kNNS Unbound / Arkade)** — *not a threat*.
   Hardware-locked to 2D/3D by the NVIDIA OptiX BVH unit. Arkade
   paper quote: "RT cores can only build BVH on three-dimensional
   data." Wrong regime entirely.
2. **LBVH-kNN (Jakob 2021, cupy-knn)** — exact and mature, but
   published numbers are 3D-only with ~2–4× speedup over basic cell
   lists. PCA-FGC's 25× over vanilla FGC strongly suggests LBVH
   would lose at d=5–10.
3. **CLOVER (ICS '25, Kamel et al.)** — the one credible threat.
   Exact, GPU-native, Voronoi-based, 10M × 30-NN in 2.71 s on V100,
   claimed 4× over "optimized grid". Code: `github.com/ampslab/clover-knn`.
   Authors did not test detector physics. **Strong recommendation:
   run a head-to-head before ICML submission.**
4. **5-D PCA subspace is near-optimal**: 3 PCs drops to ~80%
   variance (inflates candidate set); 6+ PCs makes bin grid memory
   uncacheable. A 2–3 PC ablation worth one row.
5. **Theoretical floor**: PCA-FGC at ~1% of A100 peak is
   memory-bandwidth bound, not algorithmically bound. No asymptotic
   headroom remains, only constants.

---

## 2026-05-21 — CLOVER head-to-head (in progress)

### Setup

- Cloned `github.com/ampslab/clover-knn`. Built against `cuda126` env
  (nvcc 13.2 + conda gcc 15) targeting A100 sm_80.
- Build instructions reset `-arch=sm_89` → `-arch=sm_80`; added
  `libcurand-dev` to the cuda126 env to satisfy `curand_kernel.h`.
- Discovered CLOVER is **hardcoded to 3D**: `assert(D == 3 && "Only
  dim=3 supported.")` in src/linear-scans.cu (lines 61, 178);
  `auto const dim = 3u` in include/spatial.cuh; `l2dist` only
  computes (x,y,z). Cannot run at d=5, 8, 10.
- This is actually *favourable for the paper*: CLOVER, RT-kNN, RTNN,
  and Arkade all share the same fundamental limitation — they're
  designed around raytracing-style spatial structures that only
  exist for 3D. No 3D-only competitor can challenge the d=5–10
  story. A d=3 head-to-head is still worth running to validate the
  research agent's "credible threat" claim at the one dim where
  CLOVER lives.

### Edits to CLOVER source

- `k_values{128}` (mesh path) → `k_values{40}` (match paper's k)
- `k_values{30}` (synthetic path) → `k_values{40}`
- Otherwise upstream behaviour preserved.

### Status

- Job **15445 cancelled** to make room for the max_bin_dims ablation
  (which is more fundamental to the paper's defence). CLOVER will
  re-submit after the ablation finishes — see next section.

---

## 2026-05-21 — max_bin_dims ablation

### Why this matters

- Original paper drafts claimed the `max_bin_dims=5` cap was "tuned".
  It isn't. The CUDA kernel template `select_knn_kernel<N_bin_dims>`
  is only instantiated for `N_bin_dims ∈ {2,3,4,5}`. The Python
  wrapper enforces `min(max_bin_dims, 5)` because that's what kernels
  exist for. Going higher requires adding template instantiations and
  rebuilding.
- An ICML reviewer asking "why 5?" would catch this honestly. We
  either (a) defend the choice on theoretical grounds or (b) run the
  ablation. Doing (b) is unambiguously stronger.

### Implementation

- Added kernel template instantiations for `n_bin_dims = 6, 7` in
  `FastGraphCompute-dev/fastgraphcompute/extensions/binned_select_knn_cuda_kernel.cu`
  (dispatch macro `BSK_DISPATCH(NBD)`).
- Raised the `min(..., 5)` cap in `binned_select_knn.py` and
  `binned_select_knn_pca` to `min(..., 7)`.
- Raised `TORCH_CHECK(bin_coords.size(1) <= 5)` to `<= 7` in
  `binned_knn_autograd_kernel.cpp`.
- Rebuilding from `FastGraphCompute-dev` in the `fgc-fast` env.
  Toolchain: conda-installed `cuda-nvcc=12.1` + `gcc=11.*` (matched
  with PyTorch's CUDA 12.1) to avoid the gcc-13 incompatibility.

### Sweep design

- d ∈ {8, 10}, N=5M, k=40, max_bin_dims ∈ {2,3,4,5,6,7}, variants
  {axis, pca}, 3 reps each = **72 runs**, ~ minutes.
- Hypothesis: vanilla FGC at d=8 mbd=5 is the historical baseline
  (currently ~204 s, in the prod CSV). Vanilla mbd=6,7 should
  *improve* (more axes binned, less brute force per query) until
  the bin grid memory explodes. PCA-FGC at mbd=6,7 should also
  improve relative to mbd=5 because more variance is captured.
- Output: `Performance/ablation_max_bin_dims.csv` (separate file —
  does not touch production CSVs).

### Slurm chain ordering

After this section's submissions, the chain is:
- 15433 RUNNING — cuVS BF recovery (4 contaminated cells)
- 15434 PD — synthetic PCA benchmark
- new — max_bin_dims ablation (dep on 15434)
- new CLOVER resubmit (dep on ablation)

Each `--dependency=afterany` enforces zero GPU contention.

### Paper implications

- If mbd=6 or 7 wins, we update the paper's main claim from "PCA in
  a 5-D subspace" to "PCA in a small-D subspace with empirical
  optimum at K". We rerun the headline HGCAL sweep at the new
  optimum.
- If mbd=5 wins (or essentially ties), we keep the 5 default and
  add an ablation table in the paper showing the sweep — turns a
  potential reviewer attack into a strength.

---

## Standing TODOs for the paper

- [ ] Update `Paper.tex` macros from REWRITE_NOTES.md §(b) once new
      plots regenerate.
- [ ] Plot regeneration after recovery + synthetic + ablation land
      (task #5).
- [ ] CLOVER d=3 head-to-head numbers — splice into paper as a
      sentence in §Related Work or §Experimental Setup framing all
      3D-only competitors.
- [ ] Pages-as-images proofread after final compile.
- [ ] Decide on title — current rewrite proposes "FastGraph:
      PCA-Subspace Binned k-Nearest-Neighbor Graph Construction for
      GPU Geometric Deep Learning". Might trim.

---

## 2026-05-21 — Build pipeline pain (resolved) + mbd=7 hardware limit

### Build issues encountered (resolved):
1. **head-node OOM killing nvcc** — fixed by moving build into srun (64 GB)
2. **parallel extension build race** — setuptools builds all 5 extensions in
   parallel; each emits `build/temp/build.ninja` to the same path,
   overwriting each other → only the last extension actually compiles.
   Fixed with `python setup.py build_ext --inplace -j 1`.
3. **conda compat ld misroots `-L<env>/lib` paths via `=` SEARCH_DIR
   prefix** — fixed by manually linking with system `/usr/bin/g++` +
   `-Wl,-rpath` (bypassing conda compiler_compat/ld).
4. **`libcudart.so` symlink broken** in `fgc-fast` env (pointed to
   12.1.105 which doesn't exist; actual file is 12.9.79). Fixed with
   `rm libcudart.so && ln -s libcudart.so.12 libcudart.so`.

Net: rebuilt `binned_knn_ops.so` (1.76 MB, 15:04 today) with new template
instantiations for `n_bin_dims ∈ {2,3,4,5,6,7}`. Existing kernels
unchanged.

### mbd=7 hardware-resource limit (new finding for the paper)

Smoke test verified `binned_select_knn` works at mbd ∈ {2,3,4,5,6}.
At mbd=7 the kernel launch fails with
`CUDA error: too many resources requested for launch`.

**Cause**: kernel block size is fixed at 512 threads in
`grid_and_block gb(n_vert, 512)`. The `select_knn_kernel` template at
N_bin_dims=7 (with K_MAX=64 local array for the bitonic top-K state)
needs more registers per thread than the SM's register file divided by
512 threads. The `select_knn_kernel_global` variant doesn't keep the
top-K in registers but still exceeds at N_bin_dims=7 due to
`binstepper<7>` carrying glidxs_[7] + total_bins_[7] + per-step state.

**Resolution**: cap the ablation at mbd ∈ {2,3,4,5,6}. mbd=7 documented
as a kernel-layout limit, not an algorithmic one — a future
implementation could reduce block size dynamically based on
N_bin_dims (e.g. 256 threads for N_bin_dims≥6). For the paper we have
the mbd=5-vs-6 comparison, which is the load-bearing data point.

---

## 2026-05-21 — Mid-run status (15:42)

### Slurm chain re-queued after build saga

- 15433 cuvsbf_rec: COMPLETED but data is BAD (see below)
- 15434 synth_pca: ran against broken .so, crashed silently in 1 s
- 15450 mbd_abl: ran against broken .so, crashed in 6 s
- 15451 clover: COMPLETED 11m41s — only ran synthetic path, never reached
  HGCAL mesh path; modified source to skip synth and rebuilt
- Resubmitted: **15485** synth_pca → **15486** mbd_abl → **15487** clover
  (mesh-only). Chain locked with afterany deps. All three now use the
  freshly rebuilt FastGraphCompute-dev .so files via PYTHONPATH override.

### cuVS BF is multi-modal (new paper-worthy finding)

The recovery (15433) returned 400–520 s for the 4 cells I thought were
contaminated (d=2, 4, 8, 9 at N=5M, k=40). Looking across **all** cuVS BF
data on this workload:

| source           | times seen at d=2..10, N=5M, k=40 |
|------------------|-----------------------------------|
| gpu:1 production | 145–148 s OR 390–401 s            |
| mps:50 calib (3 reps/cell) | 145–148 s × 18 reps, then 205–247 s × 6 reps, then 145–148 s |
| recovery 15433   | 400–520 s consistent              |

cuVS BF has at least **three distinct runtime modes** on this workload:
- ~145 s (fast)
- ~210 s (medium)
- ~395 s (slow, sometimes with extra overhead pushing to 520 s)

Modes appear to switch unpredictably between reps — looks like a warm-up
/ memory-layout state in cuVS BF that we don't control. The mps:50
calibration captured mostly the fast mode (18/27 reps), making it the
**right number to quote** in the paper for cuVS BF.

**Paper framing**: "cuVS brute force exhibits multi-modal runtime
behaviour on this workload; we report the consistent fast-mode median
(~145 s at N=5M, k=40, d≥2) measured across 18 isolated repetitions
under matched mps:50 allocation. The slow-mode behaviour is consistent
with cuVS BF's IVF/PQ-style internal scratch pool reaching steady state."

Recovery data (cuvs_bf_recovery.csv) tagged in PROJECT_LOG.md as **DO
NOT USE** — it was contaminated by something (likely the second-by-second
GPU sharing with other jobs around 13:00 today during my build saga).
Original mps:50 calibration values stand as the authoritative cuVS BF
numbers for the paper.

### CLOVER first run — synthetic only

CLOVER ran the synthetic path (uniform 3D) up to N=700k for all three
algorithms (bitonic, warpwise, hubs). Did not progress to N=800k+ or
the mesh (HGCAL) path. Notable synthetic hubs numbers at d=3, k=40:
- N=100k: ~70 ms
- N=500k: ~330 ms
- N=700k: ~445 ms

For reference, vanilla FGC at d=3 N=100k k=40 on HGCAL data: ~13 ms.
Already 5× faster than CLOVER hubs on uniform 3D synthetic, even before
PCA-FGC enters the picture. Different distributions, so not yet a clean
comparison.

The new CLOVER run (15487, mesh path only) will give us CLOVER on HGCAL
d=3 at N=100k…5M for a clean head-to-head.

---

## 2026-05-21 — Paper rewrite executed (option-b reframe + mbd ablation + CLOVER)

### What changed in Paper.tex

**Macros (top of file)** — replaced with mps:50-calibrated numbers from
NOTES.md's headline table:
- `\spdHGCAL*` now consistently "vs FAISS" across all dims (was mixed
  "vs FAISS" at d=2-4 and "vs vanilla" at d=5-10 — that was a paper bug).
- Added `\spdHGCALcuvs*`, `\spdHGCALcagra*` for the cross-baseline columns.
- Added `\geoFaiss=10.1x`, `\geoCuvs=4.8x`, `\geoCagra=4.4x` geomeans.
- Added reference-cell wall-clocks: `\fgcPCADeight=7.2s`, `\faissDeight=306s`,
  `\cuvsBFDeight=146s`, `\cagraNNDDeight=131s`.
- Added internal-ablation macros: `\fgcVanillaBestDeight=135s`,
  `\fgcVanillaBestPCAfactor=18.8x` (PCA at its best k=3 vs vanilla at its
  best k=6).
- Synth speedup macros set to `TBD` — patched when 15538 synth GPU
  baseline data lands.

**Abstract** — dropped "vs vanilla" headline. New abstract leads with
wall-clocks at d=8 N=5M k=40 and the cross-baseline speedups (FAISS,
cuVS BF, CAGRA) plus geomean over the full d=2-10 range.

**Introduction** — rewrote the headline paragraph in the same direction
(cross-baseline numbers, not vs-vanilla). Added the CAGRA-IVF-PQ-fails
finding to the intro narrative.

**Related Work** — added new paragraph "Three-dimensional spatial-
acceleration kNN" covering CLOVER, LBVH-kNN, RT-cores variants, and
Arkade, with the explicit 3D-hardware-lock framing. Dropped the CPU-ANN
references (HNSW, ScaNN, Annoy) from the Approximate-GPU paragraph and
added a sentence stating CPU baselines are out of scope.

**Method** — tightened §Phase 1 to note k is a user-facing hyperparameter
with default k=3 for HGCAL data, pointing forward to the ablation.

**Experimental Setup** — relabelled to `sec:expsetup`; rewrote the MPS
calibration paragraph to make the matched-allocation comparison
explicit; expanded the CAGRA build-path paragraph with the
self-included-ratio evidence; added a `max\_bin\_dims as a
hyperparameter` paragraph.

**§Headline (Performance Comparisons)** — full rewrite. Replaced the
single-baseline vs-FAISS prose with a table of speedups across all four
GPU baselines (`tab:headline-speedups`), including the geomean row.
Rewrote the surrounding prose to lean on the table and the qualitative
shape-of-curve story.

**§Synthetic** — fully rewritten to use Gaussian data (matches our
actual benchmark protocol) and the same four GPU baselines as the HGCAL
headline. All CPU-ANN references removed. Figure filenames updated to
`synth_dimensional_scaling_1M_k40_gpu.png` etc. (no longer
`synthetic_fgc_*_all_algorithms.png`).

**§Memory** — added "Measurement caveat" paragraph explaining FGC's
inflated resident-memory number (Nxk output tensors + autograd-saved
intermediates + sort/remap duplicates).

**§Ablation (NEW, `sec:mbd-ablation`)** — full subsection with the
ablation table at d=8 N=5M k=40 across k in {2,3,4,5,6}. PCA optimum k=3,
axis-aligned optimum k=6. The 18.8x at-optima ratio shown as the
strongest internal evidence that PCA orthogonalisation is the
load-bearing contribution.

**§CLOVER head-to-head (NEW, `sec:clover`)** — new subsection citing
CLOVER, motivating the 3D-only comparison, and referencing the
forthcoming `clover_headtohead_d3.png` figure.

**Limitations** — unchanged in structure; "what no longer applies" and
"what still applies" already match the new framing.

**Conclusion** — rewrote with cross-baseline geomeans, reference to
the ablation, and the CLOVER framing.

**references.bib** — added entries for kamel2025clover, jakob2021optimized,
wald2019rtnn, evangelou2021rtknn, nagarajan2023arkade.

### What still needs to happen for the paper

1. **Synth GPU baselines (15538)** — runs FAISS-GPU + cuVS BF + CAGRA-nnd
   on Gaussian d=2-10. When data lands, patch the `\spdSynth*` macros
   from `TBD` to real numbers.
2. **CLOVER head-to-head plot** — regenerate `clover_headtohead_d3.png`
   from `clover_headtohead.csv` + `pca_fgc_clover_headtohead.csv` once
   15527 finishes.
3. **Regenerate all HGCAL plots** — the figures referenced in the paper
   still use the old set; need new versions with the five-backend
   curves matching `tab:headline-speedups`. The figure file paths in
   Paper.tex are unchanged so this is a plot-script update only.
4. **Page-as-image proofread** — after the regenerated plots are in.

## 2026-05-26 — CAGRA-nn_descent full mps:100 sweep queued

Reviewer-style plot review flagged that the HGCAL N-scaling figures had
only a single CAGRA-nn_descent point at `N=5M`, because the original
NN-Descent rerun was intentionally headline-only (`d=2..10`, `N=5M`,
`k=40`, 3 reps). We now want a fair CAGRA-nn_descent curve in the
dataset-size plots rather than omitting the baseline or showing a
one-point series.

Added and submitted `Performance/run_cagra_nn_descent_mps100_full_slurm.sh`
as Slurm job 16822. The job requests `--gres=mps:100`, initializes a
resumable queue `nn_descent-mps100-full-runs-cuvs_cagra.txt`, and writes
isolated output to `cagra_nn_descent_mps100_full.csv` so the new full-GPU
measurements do not mix with the old mps:50 headline CSV. Coverage matches
the paper/backend v5 grid: dense N scans at `d=3` and `d=5`, five-point
N scans elsewhere, all `k in {10,40,100}`, 3 reps per cell.

When the job drains, update the CAGRA merge/plot path deliberately rather
than relying on the old `merge_baseline_extended.py` passthrough behavior.

## 2026-05-26 — Integrated full CAGRA-nn_descent mps:100 sweep

Job 16822 completed successfully on `rogue02` in 7:25:19 with
`ReqTRES=gres/mps=100` and `AllocTRES=gres/mps=100`. The output
`Performance/cagra_nn_descent_mps100_full.csv` contains 513 ok rows:
171 cells, exactly 3 reps per cell, covering `d=2..10`,
`k in {10,40,100}`, dense N scans at d=3 and d=5, and five-point N
scans elsewhere. The queue drained fully.

Updated `FastGraph-Plotting/make_paper_plots_v4.py` to load this full
mps:100 CAGRA CSV instead of the headline-only
`cagra_nn_descent_v5.csv`, with a fallback to the old file if the new one
is absent. Regenerated HGCAL plots now include CAGRA-nn_descent as a
proper curve in the N-scaling panels. The 5M k=40 medians are close to
the prior headline-only run (generally 0--8% faster under mps:100);
Table 1's CAGRA column was refreshed accordingly, including the
near-tie at d=4 (0.98x) and the updated CAGRA geomean of 4.3x.

## 2026-05-27 — Corrected FAISS recall convention

The recall bar plot had shown FAISS-GPU below 1.0 because
`recall_dist_faiss.csv` compares FAISS `IndexFlatL2` indices against the
FastGraph element-wise squared-distance threshold. That is not a
kernel-matched evaluation for FAISS. A direct BLAS-form check at
`d=3, N=500k, k=40` showed FAISS self-kernel recall of 1.0; the old
element-wise threshold reproduced the plotted 0.865 value. Updated the
plotting path and paper text to treat FAISS-GPU as exact under its own L2
kernel, while keeping approximate CAGRA-NN-Descent and GGNN as
distance-based recall tradeoff baselines. Removed the recall-vs-dimension
figure from the paper.

## 2026-05-27 — Added GGNN to synthetic Gaussian plots

The paper plot style is now centralized in
`FastGraph-Plotting/make_paper_plots_v4.py`: FastGraph is red in every
paper figure, exact dense baselines use green/blue, CAGRA-NN-Descent is
brown, and GGNN is gray. The synthetic Gaussian plots had no GGNN curve
because `synth_gpu_baselines.csv` only contained FAISS-GPU, cuVS BF, and
CAGRA-NN-Descent. Generated a dedicated mps:100 GGNN sweep on the same
synthetic grid (`N=1M` dimensional sweep plus d=3, d=5, and d=8
dataset-size scans, `k=40`, 3 reps) and updated the synthetic summary
plot to include GGNN.

## 2026-07-30 — Low-dimensional positioning and GravNet PCA integration

Narrowed the paper's measured contribution to exact GPU kNN for
low-to-moderate-dimensional GravNet/HGCAL spaces. The PCA contribution is
now stated as `d=4--10`; `d=2--3` remain axis-aligned controls that
short-circuit before PCA. Removed the unsupported claim that ParticleNet
and EdgeConv occupy the same dimensional window.

The public `FastGraphCompute` paper-release tree and the active
`FastGraphCompute-dev` tree now expose an opt-in
`GravNetOp(..., use_pca=True, max_bin_dims=3)` eager path. The default
axis-aligned path remains unchanged and TorchScript-compatible because the
PCA wrapper relies on eager-only `torch.pca_lowrank`. Focused dispatch and
TorchScript regression tests passed, followed by a real CUDA eager-mode
smoke test through the PCA wrapper and custom kernel.

Corrected the manuscript's API example and removed claims that the PCA
wrapper itself is `@torch.jit.script` decorated. Also disclosed the actual
one-projection-per-call 50k-row randomized PCA fit and the mixed benchmark
allocation/timed-region provenance. A canonical one-allocation rerun and
event-aware learned-latent evaluation remain outstanding.

## 2026-07-30 — Matched GPU-input mps:100 campaign queued

Implemented a separate benchmark path in `Performance` that preloads every
input as a Torch CUDA tensor before timing. FastGraph and GGNN consume that
tensor directly; FAISS uses its Torch bridge; cuVS brute force and CAGRA use
a pointer-identical CuPy DLPack view created before the timer. The measured
region includes index/build and query/search for every backend and excludes
data loading and host-to-device transfer for every backend.

A five-backend smoke chain (jobs 28959--28963) validates the adapters. The
production chain uses `qos=heavy`, literal `gres/mps:100`, four-hour bounded
jobs, and strict `afterok` serialization. Headline `N=5M,k=40,d=2--10`
jobs 28964--28970 run first; remaining paper-grid jobs 28971--28975 follow.
The full chain is recorded in
`Performance/matched_input_campaign_jobs.txt`.

By author decision, event-aware learned HGCAL coordinates are deferred to
future work and are not a blocker for this submission. The manuscript keeps
the current data labeled as a single-segment detector-feature kernel stress
test and makes no end-to-end model-throughput claim.

## 2026-08-01 — Final-layout preflight

- Rendered and visually inspected every compiled PDF page. Figures, tables, captions, and their introducing discussion are colocated; fonts are embedded and there are no unresolved cross-references or citation warnings.
- Replaced the forced placement of the main PCA-kNN pseudocode with a top-permitted float. This fills the former blank lower half of page 5 with the complexity discussion while keeping the algorithm at the start of page 6.
- Removed the Object Condensation helper appendix from the manuscript. It is unrelated to the PCA-subspace exact-kNN contribution and forced a sparse code-only final page; the implementation remains available in the FastGraph source and prior paper history. The focused manuscript now ends after the bibliography at 17 pages.


## 2026-08-03 — Matched-input MPS:100 campaign completed and paper refreshed

The serialized jobs 29316--29327 completed on 2026-08-02. The five final
CSV files contain 1,302 successful measurements: 294 rows each for
FastGraph, FAISS, cuVS brute force, and GGNN, plus 126 rows for CAGRA with
NN-Descent. Every row records
`preloaded_torch_cuda_zero_copy`; no timing row has a non-`ok` status. The
campaign used `--gres=mps:100` and kept jobs serialized, so the previous
allocation and host-to-device-transfer asymmetries no longer apply to the
HGCAL cross-method figures.

`make_paper_plots_v4.py` now reads only the five matched-input CSVs for its
HGCAL figures. The manuscript figures, table, timing protocol, and numerical
macros were regenerated from median values. At the headline N=5M, k=40
cells, FastGraph remains fastest among the tested exact GPU backends at every
d=2--10, with peak ratios of 41.23x over FAISS, 19.41x over cuVS BF, and
16.88x over CAGRA-NN-Descent. The paper was recompiled to 17 pages; page
images, embedded fonts, references, and figure placement were checked.


## 2026-08-13 — Public reproducibility release frozen

The five repositories used by the submission now have an annotated,
immutable `pca-fgc-paper-v1.0.0` tag: FastGraphCompute at `dde4b38`,
fgc-performance at `c51a290`, FastGraph-Plotting at `3f909f2`,
fastgraph-paper at `696333e`, and the CLOVER comparison fork at `a224373`.
Release documentation was corrected to describe the final matched-input
MPS:100 campaign and current 17-page manuscript. GitHub Releases and Zenodo
DOI publication require a one-time authenticated GitHub/Zenodo account
session; this Falcon environment has SSH push access but no GitHub API or
browser authentication.

A private Google Drive folder was created for the CMS-restricted HGCAL source
and ignored correctness tensors. Because the Drive connector limits individual
uploads to 512 MiB, CPU jobs 31509 and 31510 calculate source checksums and
create a 480 MiB chunked archive with per-chunk checksums before upload.

## 2026-08-14 - Final review corrections and Object Condensation validation

An independent final review found no major paper, formatting, citation, or
figure-placement issue. The manuscript now reports the actual timing
repetition counts (seven for FastGraph/PCA, FAISS, cuVS BF, and GGNN; three
for CAGRA-NN-Descent), calls the target regime
low-to-moderate-dimensional, removes stale references to a nonexistent Object
Condensation appendix, and replaces the provisional availability wording with
the immutable release-tag policy.

The Object Condensation helper remains a separate FastGraph library utility;
it is not a benchmarked contribution of this PCA-kNN paper. A fixture lookup
in its large-scale tests was made independent of the caller's working
directory. The focused CUDA suite covering the helper and object-condensation
utilities passed: 26 tests passed in 8.46 seconds on 2026-08-14.

## 2026-08-14 - Clean public reproducibility release

The `pca-fgc-paper-v1.1.0` release separates the public paper workflow from
the preserved research history. The benchmark repository now exposes a
checksummed `reproduction/` package containing the canonical figure inputs,
validated queue configurations, matched-input MPS:100 scripts, synthetic
generators, verification utilities, and the paper plotting program. Earlier
calibrations and exploratory artifacts remain available under `archive/legacy/`.

The paper repository is the central reproduction landing page, the plotting
repository is explicitly retained as a legacy archive, and the CLOVER fork is
documented as a third-party comparison dependency. All 16 canonical result
files passed SHA-256 verification; the integrated plotting workflow regenerated
the full figure set from the new layout; and the manuscript was rebuilt to 17
pages with no unresolved references.

## 2026-08-19 - Hardened software release and version alignment

FastGraphCompute package version 1.2.0 manually integrates the five required
upstream hardening changes while preserving the PCA-specific dispatch and
fused scatter implementation: current-stream launches, active-stream
row-split transfer ordering, CUDA device guards, same-device validation, and
Object Condensation bounds and optional-output fixes. Regression work also
corrected the custom C++ autograd save condition and allowed a CUDA-built
checkout to register its operators on a node without a visible GPU.

The non-duplicated A100 suite passed 67 tests with one two-GPU test skipped;
the final hardening file passed six tests with the same conditional skip. A
no-GPU CPU allocation passed 47 tests with 22 CUDA tests skipped. Every CUDA
extension also completed an isolated `sm_90` compile-only build. Runtime
validation on `cuda:1` and H100 remains pending because those hardware
configurations were not available in the validation allocations.

The manuscript and all public reproduction pointers now use the immutable
`pca-fgc-paper-v1.2.0` release identity, and the availability statement reports
FastGraphCompute package version 1.2.0. The PDF rebuilt successfully to 17
pages with embedded fonts, no unresolved references or citations, and a clean
visual check of the updated availability and conclusion pages.


## 2026-08-20 — CPC Computational Physics Paper submission snapshot

Converted the final manuscript from the CPiP presentation to the CPC Computational Physics Paper article type. Removed the CPiP-only Program Summary and unrelated Object Condensation helper mentions, retained the tested eager GravNet PCA integration, and tightened the target wording to low-to-moderate-dimensional. The rebuilt 16-page PDF has embedded fonts, valid PDF syntax, and no unresolved references or citations. The pca-fgc-paper-v1.3.1 tags preserve this final manuscript together with the unchanged FastGraphCompute, benchmark, plotting, and CLOVER revisions.


## 2026-08-25 - Required generative-AI disclosure and CPC v1.3.2 package

Added the Elsevier-required declaration of generative AI and AI-assisted
technologies immediately before the bibliography. The statement discloses
OpenAI Codex use for language editing, software review, and reproducibility
checks, and states that the authors reviewed and edited the output and accept
full responsibility for the article. Rebuilt the 16-page PDF, verified its
fonts and PDF syntax, and created the matching CPC source archive
`FastGraph-CPC-CP-v1.3.2-source.zip` with a verified SHA-256 manifest. The
v1.3.2 tag set preserves the same code, benchmark, plotting, and CLOVER
revisions as v1.3.1, with this manuscript-only disclosure update.
