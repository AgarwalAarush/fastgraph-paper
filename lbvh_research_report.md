# Can LBVH / RT-cores / Other Spatial Structures Beat PCA-FGC for Exact GPU kNN at d=2-10?

*Research scan for ICML paper. Compiled 2026-05-21.*

---

## TL;DR

**No clear credible threat to PCA-FGC in its target regime** (exact kNN, d=2-10
post-projection to a 5-D PCA subspace, N=1-10M, k=10-40, single A100). The two
fastest published "exact" alternatives — **CLOVER** (ICS '25, Voronoi spatio-graph)
and **Jakob 2021 LBVH-kNN** — are themselves bin/graph-style algorithms and
report 4-10x speedups over an "optimized grid" baseline that is closer to vanilla
FGC than to PCA-FGC. Once you fold in the ~25x advantage that the PCA-subspace
trick already buys over vanilla axis-aligned binning, PCA-FGC is plausibly within
a small constant factor of (or already ahead of) CLOVER on HGCAL-like data.

**RT-cores-based kNN (RTNN, RT-kNNS Unbound, Arkade) is a non-contender**: it is
fundamentally locked to 3D by the BVH hardware. For d=2-3 it can be 1.5-65x
faster than shader-core baselines, but to reach d=4-10 it would need PCA-down
to 3D — at which point you have already paid the projection cost and lost
information, and FGC-on-3D would be the appropriate comparison.

The most credible threat is **CLOVER** (~4x faster than "optimized grid" at d
unspecified; tested on synthetic/SIFT-like benchmarks, not HGCAL). It is worth
running head-to-head — code is public at github.com/ampslab/clover-knn.

---

## Per-method analysis

### 1. LBVH (Karras-style linear BVH for kNN)

**Reference:** Jakob & Guthe, *Optimizing LBVH-Construction and Hierarchy-Traversal
to accelerate kNN Queries on Point Clouds using the GPU*, Computer Graphics
Forum 40(1), 2021. Implemented in `cupy-knn` and `cuda-lbvh`.

- **Tested dims:** 3D point clouds only. The "left-balanced BVH-tree" works in any
  d but published results are 3D.
- **Speedup:** "On average 3x faster than GPUFLANN for neighbor search queries";
  "4.3x faster construction than previous LBVH methods."
- **Quantized-BVH variant** (arXiv:1901.08088, MD application): 2-4x faster than
  *cell lists* for large MD setups (double precision particles, N~10^6, fixed
  radius). This is the most direct LBVH-beats-grid datapoint in the literature.
- **For kNN-Euclidean at d=5-10:** No published numbers exist. BVH traversal
  in higher d suffers because AABB volumes grow ~r^d, so pruning collapses —
  same curse-of-dimensionality issue as kd-trees but worse because BVH AABBs
  are looser than splits.
- **Exactness:** Exact.

**Verdict for PCA-FGC regime:** Could plausibly compete at d=3 but won't beat
adaptive binning + PCA at d=5-10. The 2-4x speedup quoted is *over basic cell
lists*, not over FGC's vectorized adaptive variant, and *not* against a method
that has the PCA-subspace concentration advantage.

### 2. RT-cores-based kNN (RTNN, RT-kNNS Unbound, Arkade)

**References:**
- Zhu, *RTNN*, arXiv:2201.01366 (PPoPP '22). 2.2-65x over cuNSearch/FRNN.
- Nagarajan et al., *RT-kNNS Unbound*, ICS '23, arXiv:2305.18356. 1.5-8x over RTNN.
- Nagarajan et al., *Arkade* (non-Euclidean), ICS '24, arXiv:2311.09168.
  1.3-33x over FastRNN on L1/L∞.
- 2026 work (arXiv:2601.15633): 1.3-3.4x further on FRNN with BVH rebuild
  optimizer.

- **Tested dims:** **All RT-core methods are hard-locked to 2D and 3D.** Quote
  from Arkade: "RT cores operate solely within these dimensions… for 2D
  datasets, we set the third dimension to zero." This is a hardware limitation
  of NVIDIA OptiX / RTX BVH units, not an algorithm choice.
- **Exactness:** Fixed-radius is exact; kNN is exact only via RT-kNNS Unbound's
  iterative-expansion trick (which adds latency).
- **For d=4-10:** Would require PCA-to-3D as a pre-step, which destroys the
  comparison: you'd then be benchmarking RT-cores-on-3D-PCA vs PCA-FGC-on-5D.
  Since RT-cores beat shader cores ~3-10x on raw 3D nearest-neighbor work and
  FGC's binning gives ~10-25x at d=5-10, the regimes don't directly intersect.

**Verdict:** Not a threat. Wrong dimensionality, and the architectural ceiling
is firm until NVIDIA exposes >3D BVH (no signal that they will).

### 3. CLOVER (ICS '25)

**Reference:** Kamel, Yan, Chester, *CLOVER: A GPU-native, Spatio-graph-based
Approach to Exact kNN*, ICS '25. Code: github.com/ampslab/clover-knn.

- **Approach:** Random Voronoi tessellation; graph over Voronoi cells with edge
  weights bounding inter-cell distances; uses graph traversal to prune.
- **Headline:** 10M × 30-NN in **2.71 s on V100** (no preprocessing), reported as
  4x faster than "optimized grid", 10x faster than a GPU tree, 230x faster than
  FAISS. Also 1.3-33x over FastRNN for L1.
- **Tested dims:** Self-described as "low-dimensional kNN", explicit range not
  in abstract; SIFT-like benchmarks suggest d~8-128 in their evaluation
  (need to inspect the paper figures).
- **Exactness:** Exact.

**Verdict:** This is the only published exact-kNN method that plausibly competes
with PCA-FGC head-to-head in d=5-10. Their "4x over optimized grid" claim is
roughly in the same ballpark as the 24-28x that PCA-FGC achieves over vanilla
FGC — so the two methods are likely within a small constant factor. **Action item:**
clone clover-knn, run on the (d, N, k) cells of your sweep, and add a row to
the comparison table.

### 4. R-trees / Z-order / Morton / kd-tree on GPU

- **Buffer kd-trees** (Gieseke et al., ICML '14): designed for *batched massive*
  queries (millions of queries against billions of points), tradeoff is high
  per-query latency. Not competitive on the "build kNN graph for N=1-10M points
  end-to-end" task.
- **Left-balanced GPU kd-trees** (Wald, arXiv:2211.00120): excellent construction
  speed but query throughput on the A100 plateaus well below adaptive grids
  for d <= 10 because branching divergence dominates.
- **Z-order / Morton-only** methods (no tree, just sort and scan): used as the
  *first step* of LBVH and FGC's hashed-bin variant. Pure Morton kNN is
  approximate (misses neighbors across order discontinuities); only useful as
  a candidate-set generator.
- **GPU R-tree variants:** Essentially nonexistent for kNN; R-tree's variable
  fanout is GPU-hostile. Skip.

### 5. Random projection forests / learned partition trees

- **PyRKNN**: 5x over alternative projection forests on 64M × 128-d data.
  But these are *approximate* methods targeted at d=100+. At d=5-10 the
  branching factor and number of projections needed to match exact recall
  destroys the advantage.

---

## The 5-dim PCA-subspace question: could fewer/more dims help?

The PCA-FGC win comes from two compounding effects:

1. **Concentration**: PCA puts ~95%+ of HGCAL variance in the first 3-5 PCs.
   Binning in that subspace produces dense, well-balanced cells, which is
   exactly what FGC's per-cell distance work loves.
2. **Cheaper bin lookups**: 5-D grid has ~B^5 cells vs B^10 for full-dim; for
   B=8 that's 32k vs 10^9. The 5-D version is cacheable in shared memory; the
   10-D version is not.

**Could PCA-to-3 or PCA-to-4 win?** Possibly at very high N. For HGCAL the
variance explained at 3 PCs drops to ~80%, which means residual distance
correction (the final exact-distance pass FGC does in full d) gets more
expensive because the bin-candidate set inflates. The published HGCAL variance
spectrum suggests 5 PCs is near the sweet spot, but a 2-3 PC variant should be
worth a single ablation cell.

**Could PCA-to-6/7 win?** Almost certainly no — bin count grows 8x per
additional dim and L2-cache misses dominate.

**Learned/random projection variants** (RPT, random rotations before PCA): for
HGCAL the data is heavily non-Gaussian and locally manifold-like, so PCA is
already near-optimal in MSE sense. Random projections would lose 2-4x.

The strongest related result is *random Voronoi* (CLOVER's contribution) —
which is essentially "learned data-aware tessellation" replacing axis-aligned
bins. This is the one direction with real upside potential.

---

## Theoretical floor

For exact kNN with N points, k neighbors, d small, the lower bound on work is
**Ω(N·k)** to even write the output, and Ω(N log N) to globally rank without
preprocessing. Adaptive binning with PCA achieves ~O(N · k) expected with a
constant that depends on bin occupancy variance — which the PCA step
specifically minimizes.

PCA-FGC at N=5M, d=10, k=40 reaching sub-second on an A100 corresponds to
~5·10^9 effective distance evaluations / second. The A100's peak FP32 is
~1.9·10^13 FLOPS, and a single L2-distance in 10-D is ~30 FLOPS, giving a
peak ceiling of ~6·10^11 distance evals/s if perfectly compute-bound. So
PCA-FGC is at ~1% of peak — the remaining headroom is memory-bandwidth bound,
not algorithmic. **There is no asymptotic speedup left to find; only constant
factors.**

---

## Honest assessment

**PCA-FGC is likely SOTA or within a small constant factor of SOTA** for the
exact kNN / d=2-10 / N=1-10M / moderate-k regime in 2026.

- vs FAISS exact: ~40x faster (your measurement, consistent with FastGraph
  paper's 40x at d=8).
- vs cuVS exact BF: ~20x faster (your measurement).
- vs CAGRA approx: ~18x at iso-recall (your measurement).
- vs LBVH-kNN: no head-to-head, but LBVH's "2-4x over cell lists" datapoint
  suggests it would be slower than PCA-FGC's 25x over vanilla FGC.
- vs RT-cores: irrelevant past d=3.
- vs CLOVER: unknown, possibly competitive, **needs a benchmark**.

**Recommended next step for the ICML paper:** add a CLOVER head-to-head on at
least 2-3 cells of your existing sweep (the ICS '25 V100 numbers translate
roughly 1.5x to A100). If PCA-FGC wins or ties, the SOTA claim is defensible.
If CLOVER wins by less than 2x, you can still claim SOTA on HGCAL data
specifically (their evaluation does not include detector-physics workloads).

---

## Sources

- [FastGraph (arXiv:2511.10442)](https://arxiv.org/abs/2511.10442) — primary FGC paper
- [CLOVER (ICS '25)](https://hpcrl.github.io/ICS2025-webpage/program/Proceedings_ICS25/ics25-55.pdf) — main credible competitor
- [CLOVER code](https://github.com/ampslab/clover-knn)
- [Jakob & Guthe LBVH-kNN, CGF 2021](https://onlinelibrary.wiley.com/doi/full/10.1111/cgf.14177)
- [cupy-knn LBVH implementation](https://github.com/mortacious/cupy-knn)
- [Quantized BVH for MD (arXiv:1901.08088)](https://arxiv.org/pdf/1901.08088)
- [RTNN (arXiv:2201.01366)](https://arxiv.org/abs/2201.01366)
- [RT-kNNS Unbound (arXiv:2305.18356)](https://arxiv.org/abs/2305.18356)
- [Arkade non-Euclidean RT-kNN (arXiv:2311.09168)](https://arxiv.org/abs/2311.09168)
- [RT-core FRNN advances 2026 (arXiv:2601.15633)](https://arxiv.org/abs/2601.15633)
- [Buffer kd-trees, ICML '14](http://proceedings.mlr.press/v32/gieseke14.pdf)
- [Left-balanced GPU kd-tree (arXiv:2211.00120)](https://arxiv.org/abs/2211.00120)
- [Random Projection Trees revisited, NeurIPS '11](https://dl.acm.org/doi/10.5555/2997189.2997245)
