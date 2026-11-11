# FastGraph local results: evidence and limits

Author-review draft. Original results and manuscript figures are unchanged.

Sources: 2 plans; 4,185 measured timing/quality rows.
Ratios pair identical inputs, K, GPU identity and source plan. Each point uses the median of its measured repetitions.
Ranges below are observed seed ranges, not confidence intervals. Speed/recall rows come from the same query settings.
Repeated control blocks with the same input hash are collapsed before seed summaries; the case-level CSV retains every paired block.

## Source coverage

| Scope | Complete bundles | Failed | Missing |
|---|---:|---:|---:|
| synthetic | 421 | 0 | 0 |
| local-extension | 654 | 1 | 13 |

## Default three-bin-dimensional solver, N=1 million

Ratio >1 favors PCA-FastGraph. All times include index construction plus query/output conversion.

| Distribution | d | K | Seeds | PCA seconds | cuVS/PCA range | FAISS/PCA range | Axis/PCA range |
|---|---:|---:|---:|---:|---:|---:|---:|
| anisotropic_0.50 | 8 | 40 | 1 | 5.626 | 1.18–1.18 | 2.25–2.25 | 1.25–1.25 |
| anisotropic_0.50 | 10 | 40 | 1 | 8.342 | 0.80–0.80 | 1.52–1.52 | 1.43–1.43 |
| anisotropic_0.90 | 4 | 40 | 3 | 0.563 | 10.36–11.79 | 19.96–22.68 | 0.97–1.12 |
| anisotropic_0.90 | 8 | 40 | 3 | 1.383 | 4.76–4.91 | 9.08–9.39 | 3.32–4.97 |
| anisotropic_0.90 | 10 | 40 | 3 | 2.034 | 3.22–3.30 | 6.12–6.28 | 3.52–4.58 |
| anisotropic_0.99 | 4 | 40 | 3 | 0.250 | 24.28–26.86 | 46.75–51.70 | 0.98–1.08 |
| anisotropic_0.99 | 8 | 10 | 2 | 0.231 | 23.85–24.94 | 36.67–38.34 | 7.38–13.53 |
| anisotropic_0.99 | 8 | 40 | 3 | 0.300 | 21.74–22.81 | 41.52–43.56 | 8.51–13.09 |
| anisotropic_0.99 | 8 | 100 | 2 | 0.493 | 32.52–32.89 | 26.84–27.13 | 6.95–11.21 |
| anisotropic_0.99 | 10 | 10 | 2 | 0.297 | 18.24–19.96 | 28.62–31.41 | 9.30–18.83 |
| anisotropic_0.99 | 10 | 40 | 3 | 0.362 | 17.41–18.50 | 33.16–35.24 | 9.88–18.77 |
| anisotropic_0.99 | 10 | 100 | 2 | 0.555 | 30.01–30.03 | 24.22–24.24 | 8.72–15.22 |
| gaussian | 4 | 40 | 3 | 0.778 | 8.13–8.98 | 15.66–17.27 | 1.00–1.08 |
| gaussian | 8 | 10 | 2 | 5.468 | 1.03–1.03 | 1.58–1.59 | 1.00–1.02 |
| gaussian | 8 | 40 | 3 | 7.151 | 0.92–0.93 | 1.76–1.78 | 0.99–1.00 |
| gaussian | 8 | 100 | 2 | 9.087 | 1.77–1.78 | 1.46–1.47 | 0.99–1.00 |
| gaussian | 10 | 10 | 2 | 10.417 | 0.54–0.55 | 0.85–0.86 | 1.00–1.01 |
| gaussian | 10 | 40 | 3 | 12.389 | 0.53–0.54 | 1.01–1.02 | 1.00–1.01 |
| gaussian | 10 | 100 | 2 | 14.485 | 1.15–1.15 | 0.93–0.93 | 0.99–1.00 |
| gaussian_unit_trace | 8 | 40 | 1 | 7.254 | 0.92–0.92 | 1.75–1.75 | 0.99–0.99 |
| gaussian_unit_trace | 10 | 40 | 1 | 12.469 | 0.53–0.53 | 1.01–1.01 | 0.99–0.99 |

Replication details and exploratory across-seed intervals are in UNCERTAINTY.md; observed seed ranges above are not confidence intervals.

## Correctness and approximate methods

Recalls are distance-based with the documented tolerance; full and sampled reference coverage remain distinct.
FGC pass includes strict distance-multiset/returned-distance checks. Other backends' pass flags enforce structural validity only; an ok record is not evidence of recall 1 or numerical agreement with FP64.

- cagra_nnd: 1170 rows; recall 0.999951–1.000000; 0 failed recorded checks.
- cuvs_bf: 312 rows; recall 0.988353–1.000000; 0 failed recorded checks.
- faiss: 276 rows; recall 0.990107–1.000000; 0 failed recorded checks.
- fgc_axis: 516 rows; recall 1.000000–1.000000; 0 failed recorded checks.
- fgc_pca: 711 rows; recall 1.000000–1.000000; 0 failed recorded checks.
- ggnn: 1200 rows; recall 0.589908–1.000000; 0 failed recorded checks.

CAGRA settings may saturate at full sampled recall; this does not prove exactness or establish a broad recall trade-off.
Approximate methods are not treated as exact merely because sampled recall is 1.

## Bin dimension and PCA sample ablations

Best means the fastest observed configuration on the same input, not an independently validated universal optimum.

| Distribution | d | N | K | Default ms | Best ms | Best bins | PCA sample | Default/best |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gaussian | 8 | 100,000 | 40 | 226.91 | 117.41 | 2 | 2000 | 1.93 |
| anisotropic_0.90 | 8 | 100,000 | 40 | 43.59 | 40.16 | 3 | 2000 | 1.09 |
| anisotropic_0.99 | 8 | 100,000 | 40 | 22.27 | 22.27 | 3 | 50000 | 1.00 |
| gaussian | 10 | 100,000 | 40 | 469.50 | 179.90 | 2 | 2000 | 2.61 |
| anisotropic_0.90 | 10 | 100,000 | 40 | 49.83 | 48.38 | 3 | 2000 | 1.03 |
| anisotropic_0.99 | 10 | 100,000 | 40 | 21.92 | 20.86 | 3 | 2000 | 1.05 |
| gaussian | 8 | 1,000,000 | 40 | 7200.39 | 7136.62 | 3 | 2000 | 1.01 |
| anisotropic_0.99 | 8 | 1,000,000 | 40 | 300.73 | 300.73 | 3 | 50000 | 1.00 |
| anisotropic_0.99 | 8 | 100,000 | 10 | 12.36 | 12.36 | 3 | 50000 | 1.00 |
| anisotropic_0.99 | 8 | 100,000 | 100 | 36.08 | 34.69 | 3 | 2000 | 1.04 |
| gaussian | 10 | 1,000,000 | 40 | 12409.47 | 11856.90 | 2 | 2000 | 1.05 |
| anisotropic_0.99 | 10 | 1,000,000 | 40 | 381.91 | 381.91 | 3 | 50000 | 1.00 |
| anisotropic_0.99 | 10 | 100,000 | 10 | 14.89 | 13.87 | 3 | 2000 | 1.07 |
| anisotropic_0.99 | 10 | 100,000 | 100 | 35.86 | 35.86 | 3 | 50000 | 1.00 |

Ablation panels presently use one independent seed with repeated timing measurements; that is weaker than cross-seed tuning validation.

## Memory measurements

Absolute peaks include the process/allocator baseline. Deltas alone can hide allocations retained from warmup.

| Distribution | N | Method | Absolute peak GiB | Baseline GiB | Delta GiB | Samples |
|---|---:|---|---:|---:|---:|---:|
| gaussian (raw) | 1,000,000 | fgc_pca | 2.379 | 1.332 | 1.047 | 3385 |
| gaussian (raw) | 1,000,000 | fgc_axis | 2.338 | 1.268 | 1.070 | 3424 |
| gaussian (raw) | 1,000,000 | faiss | 4.010 | 1.268 | 2.742 | 6007 |
| gaussian (raw) | 1,000,000 | cuvs_bf | 2.320 | 1.270 | 1.051 | 3160 |
| gaussian (raw) | 1,000,000 | cagra_nnd | 2.440 | 1.270 | 1.170 | 25457 |
| gaussian (raw) | 1,000,000 | ggnn | 2.141 | 1.268 | 0.873 | 1977 |
| anisotropic_0.99 (raw) | 1,000,000 | fgc_pca | 2.379 | 1.332 | 1.047 | 149 |
| anisotropic_0.99 (raw) | 1,000,000 | fgc_axis | 2.338 | 1.268 | 1.070 | 1199 |
| anisotropic_0.99 (raw) | 1,000,000 | faiss | 4.010 | 1.268 | 2.742 | 5997 |
| anisotropic_0.99 (raw) | 1,000,000 | cuvs_bf | 2.022 | 1.270 | 0.752 | 3159 |
| anisotropic_0.99 (raw) | 1,000,000 | cagra_nnd | 2.440 | 1.270 | 1.170 | 25695 |
| anisotropic_0.99 (raw) | 1,000,000 | ggnn | 2.291 | 1.268 | 1.023 | 1693 |
| anisotropic_0.50 (raw) | 1,000,000 | fgc_pca | 2.379 | 1.332 | 1.047 | 2641 |
| anisotropic_0.50 (raw) | 1,000,000 | fgc_axis | 2.338 | 1.268 | 1.070 | 3333 |
| detector_feature_prefix (raw) | 1,000,000 | fgc_pca | 2.379 | 1.332 | 1.047 | 220 |
| detector_feature_prefix (raw) | 1,000,000 | fgc_axis | 2.338 | 1.268 | 1.070 | 7890 |
| detector_feature_prefix (standardized) | 1,000,000 | fgc_pca | 2.379 | 1.332 | 1.047 | 7224 |
| detector_feature_prefix (standardized) | 1,000,000 | fgc_axis | 2.338 | 1.268 | 1.070 | 5234 |

## Search pruning, memory and gradients

| Distribution | N | Method | Candidates/query | Candidate fraction of all eligible non-self pairs |
|---|---:|---|---:|---:|
| gaussian (raw) | 100,000 | fgc_pca | 40,506 | 40.5065% |
| gaussian (raw) | 100,000 | fgc_axis | 41,370 | 41.3702% |
| anisotropic_0.99 (raw) | 100,000 | fgc_pca | 2,484 | 2.4841% |
| anisotropic_0.99 (raw) | 100,000 | fgc_axis | 18,675 | 18.6755% |
| gaussian (raw) | 1,000,000 | fgc_pca | 268,811 | 26.8811% |
| gaussian (raw) | 1,000,000 | fgc_axis | 273,728 | 27.3728% |
| anisotropic_0.99 (raw) | 1,000,000 | fgc_pca | 23,490 | 2.3490% |
| anisotropic_0.99 (raw) | 1,000,000 | fgc_axis | 95,598 | 9.5598% |
| anisotropic_0.50 (raw) | 100,000 | fgc_pca | 33,609 | 33.6092% |
| anisotropic_0.50 (raw) | 100,000 | fgc_axis | 40,014 | 40.0147% |
| anisotropic_0.50 (raw) | 1,000,000 | fgc_pca | 208,191 | 20.8192% |
| anisotropic_0.50 (raw) | 1,000,000 | fgc_axis | 263,335 | 26.3335% |
| gaussian_unit_trace (raw) | 65,536 | fgc_pca | 968 | 94.6258% |
| gaussian_unit_trace (raw) | 65,536 | fgc_axis | 972 | 95.0034% |
| anisotropic_0.99 (raw) | 65,536 | fgc_pca | 501 | 49.0103% |
| anisotropic_0.99 (raw) | 65,536 | fgc_axis | 750 | 73.3214% |
| detector_feature_prefix (raw) | 1,000,000 | fgc_pca | 37,516 | 3.7516% |
| detector_feature_prefix (raw) | 1,000,000 | fgc_axis | 999,608 | 99.9609% |
| detector_feature_prefix (standardized) | 1,000,000 | fgc_pca | 890,467 | 89.0468% |
| detector_feature_prefix (standardized) | 1,000,000 | fgc_axis | 998,906 | 99.8907% |

Largest fixed-neighbor autograd gradient discrepancy: 1.4e-09.
Largest observed repeat gradient discrepancy: 9.31e-10.
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
