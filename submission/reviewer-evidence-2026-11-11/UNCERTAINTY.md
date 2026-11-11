# Replication and uncertainty audit

Each timing point is the median of its recorded repetitions after the configured warmup. Repeated timings share an input and are not independent data seeds. Repeated input hashes across control panels are collapsed.

`timing-repeatability.csv` reports repetition count, inclusive quartiles and observed range per measured configuration. These are descriptive timing variability, not a confidence interval.

`seed-uncertainty.csv` uses one paired baseline/PCA median-time ratio per independent data seed. The center is exp(mean(log ratio)); the exploratory 95% interval is exp(mean ± t(0.975,n−1) × sd/sqrt(n)). For n>10 the df=9 critical value gives a conservative interval under the same model. This assumes independent, approximately normal seed log ratios. With only two or three seeds that assumption cannot be assessed reliably. These pointwise intervals have no multiple-comparison correction, do not certify unseen data, and do not cover systematic hardware/protocol errors or application generalization. One-input cases have no across-input CI.

## Independent-input coverage

| Seeds per matched cell | Cells |
|---:|---:|
| 1 | 18 |
| 2 | 8 |
| 3 | 18 |

## Selected million-point K=40 synthetic comparisons against cuVS

These intervals estimate the geometric mean speedup within each specified generator, not across all workloads.

| Distribution | d | Seeds | Geometric speedup | Exploratory 95% interval |
|---|---:|---:|---:|---|
| anisotropic_0.50 | 8 | 1 | 1.18 | unavailable |
| anisotropic_0.50 | 10 | 1 | 0.80 | unavailable |
| anisotropic_0.90 | 4 | 3 | 11.28 | 9.39–13.54 |
| anisotropic_0.90 | 8 | 3 | 4.82 | 4.63–5.02 |
| anisotropic_0.90 | 10 | 3 | 3.26 | 3.16–3.37 |
| anisotropic_0.99 | 4 | 3 | 25.82 | 22.58–29.53 |
| anisotropic_0.99 | 8 | 3 | 22.21 | 20.89–23.61 |
| anisotropic_0.99 | 10 | 3 | 18.09 | 16.65–19.65 |
| gaussian | 4 | 3 | 8.53 | 7.54–9.64 |
| gaussian | 8 | 3 | 0.93 | 0.92–0.93 |
| gaussian | 10 | 3 | 0.53 | 0.53–0.54 |
| gaussian_unit_trace | 8 | 1 | 0.92 | unavailable |
| gaussian_unit_trace | 10 | 1 | 0.53 | unavailable |

Numerical correctness samples are a different question: query samples are not timing replications or independent model runs. The current campaigns contain no independent trained-model repetitions or confirmed real-event cohorts.
