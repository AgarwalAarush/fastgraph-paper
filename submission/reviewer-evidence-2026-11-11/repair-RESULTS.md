# FastGraph local results: evidence and limits

Author-review draft. Original results and manuscript figures are unchanged.

Sources: 1 plans; 522 measured timing/quality rows.
Ratios pair identical inputs, K, GPU identity and source plan. Each point uses the median of its measured repetitions.
Ranges below are observed seed ranges, not confidence intervals. Speed/recall rows come from the same query settings.
Repeated control blocks with the same input hash are collapsed before seed summaries; the case-level CSV retains every paired block.

## Source coverage

| Scope | Complete bundles | Failed | Missing |
|---|---:|---:|---:|
| local-repair | 152 | 0 | 0 |

## Default three-bin-dimensional solver, N=1 million

Ratio >1 favors PCA-FastGraph. All times include index construction plus query/output conversion.

| Distribution | d | K | Seeds | PCA seconds | cuVS/PCA range | FAISS/PCA range | Axis/PCA range |
|---|---:|---:|---:|---:|---:|---:|---:|

Replication details and exploratory across-seed intervals are in UNCERTAINTY.md; observed seed ranges above are not confidence intervals.

## Correctness and approximate methods

Recalls are distance-based with the documented tolerance; full and sampled reference coverage remain distinct.
FGC pass includes strict distance-multiset/returned-distance checks. Other backends' pass flags enforce structural validity only; an ok record is not evidence of recall 1 or numerical agreement with FP64.

- cagra_nnd: 144 rows; recall 1.000000–1.000000; 0 failed recorded checks.
- cuvs_bf: 36 rows; recall 0.998846–1.000000; 0 failed recorded checks.
- faiss: 36 rows; recall 0.999059–1.000000; 0 failed recorded checks.
- fgc_axis: 81 rows; recall 1.000000–1.000000; 0 failed recorded checks.
- fgc_pca: 81 rows; recall 1.000000–1.000000; 0 failed recorded checks.
- ggnn: 144 rows; recall 0.589973–0.999945; 0 failed recorded checks.

CAGRA settings may saturate at full sampled recall; this does not prove exactness or establish a broad recall trade-off.
Approximate methods are not treated as exact merely because sampled recall is 1.

## Bin dimension and PCA sample ablations

Best means the fastest observed configuration on the same input, not an independently validated universal optimum.

| Distribution | d | N | K | Default ms | Best ms | Best bins | PCA sample | Default/best |
|---|---:|---:|---:|---:|---:|---:|---:|---:|

Ablation panels presently use one independent seed with repeated timing measurements; that is weaker than cross-seed tuning validation.

## Memory measurements

Absolute peaks include the process/allocator baseline. Deltas alone can hide allocations retained from warmup.

| Distribution | N | Method | Absolute peak GiB | Baseline GiB | Delta GiB | Samples |
|---|---:|---|---:|---:|---:|---:|

## Search pruning, memory and gradients

| Distribution | N | Method | Candidates/query | Candidate fraction of all eligible non-self pairs |
|---|---:|---|---:|---:|
| gaussian_unit_trace (raw) | 65,536 | fgc_pca | 968 | 94.6258% |
| gaussian_unit_trace (raw) | 65,536 | fgc_axis | 972 | 95.0034% |
| anisotropic_0.99 (raw) | 65,536 | fgc_pca | 501 | 49.0103% |
| anisotropic_0.99 (raw) | 65,536 | fgc_axis | 750 | 73.3214% |

Largest fixed-neighbor autograd gradient discrepancy: 5.09e-11.
Largest observed repeat gradient discrepancy: 2.91e-11.
These are bounded diagnostics on prefixes with fixed seeds, not bitwise determinism or a GNN training-accuracy claim.

Memory tables retain absolute sampled peaks AND baseline/delta. Warm allocator state can make a small delta misleading.
NVML is sampled device-wide; profiling/counter timings are excluded from latency comparisons.

## What remains unmeasured

- Actual learned GravNet coordinates and complete model training/inference throughput: no usable trained checkpoint/adapter supplied.
- Confirmed event-batched HGCAL: offset semantics and physical feature definitions remain unconfirmed.
- H100 runtime: local results are A100 measurements.
- Full-graph numerical correctness for million-point inputs: large references cover recorded queries against all eligible candidates.
- Reconstruction accuracy, convergence and energy/shower response: no such result is implied by these kernel timings.

Synthetic equal-size segments and unsegmented feature stress remain explicitly labeled surrogates/stress tests.
Raw/standardized inputs define different metrics and retain separate reference/input identities.
The original Gaussian has covariance trace d; new unit-trace Gaussian controls match anisotropic trace 1.
Bin/PCA-sample configurations selected by observed timings are exploratory in-sample choices, not an independently validated universal optimum.
