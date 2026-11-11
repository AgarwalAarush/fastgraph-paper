# Returned result coverage

Source plan: `ee6135bac6fcb7b645f707a7e6a0068d215f76296d5e9daf5e8e9859e53b18f1`

Profile: focused; scope: local-repair

| Stage/backend | Complete | Failed | Missing |
|---|---:|---:|---:|
| benchmark/cagra_nnd | 12 | 0 | 0 |
| benchmark/cuvs_bf | 12 | 0 | 0 |
| benchmark/faiss | 12 | 0 | 0 |
| benchmark/fgc_axis | 27 | 0 | 0 |
| benchmark/fgc_pca | 27 | 0 | 0 |
| benchmark/ggnn | 12 | 0 | 0 |
| counters/fgc_axis | 2 | 0 | 0 |
| counters/fgc_pca | 2 | 0 | 0 |
| prepare/core | 17 | 0 | 0 |
| profile/cagra_nnd | 2 | 0 | 0 |
| profile/cuvs_bf | 2 | 0 | 0 |
| profile/faiss | 2 | 0 | 0 |
| profile/fgc_axis | 2 | 0 | 0 |
| profile/fgc_pca | 2 | 0 | 0 |
| profile/ggnn | 2 | 0 | 0 |
| reference/core | 17 | 0 | 0 |

## Scientific priority coverage

| Phase | Complete | Failed | Missing |
|---|---:|---:|---:|
| checks | 40 | 0 | 0 |
| controls-core | 8 | 0 | 0 |
| breadth | 104 | 0 | 0 |

Strategy: reverse; status: complete; peer-covered bundles: 0.
Peer results count only as separate whole-case evidence; local missing rows stay missing.
Deferred units: 0; unresolved unit failures: 0.

Partial runs remain partial. Review failed/missing stages before claiming coverage.
Large-input recall uses the recorded query sample; it is not a full-graph certificate.
H100 and historical A100 results must remain separate. Original audit artifacts stay with the operator.
Derived results still require author review before Git publication.
