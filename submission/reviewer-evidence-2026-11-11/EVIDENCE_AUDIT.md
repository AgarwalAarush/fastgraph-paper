# Reviewer evidence audit — November 11, 2026

This maps the saved Array-review summary, not the unavailable original
numbered reports or Reviewer 18 attachment. It cannot certify a complete
point-by-point response. The earlier CPC framing decision is separate.

| Requested evidence | Local status | Remaining limitation or dependency |
|---|---|---|
| Genuine event-preserving batches | Synthetic segmented measurements collected | Data owner must confirm offsets/order against the feature matrix; synthetic segments are not detector events |
| Trained learned coordinates | Not collected | Real model/checkpoints, meaningful task batches/loss, and capture adapter required |
| Feature-scale and covariance controls | Raw/standardized numerical stress, isotropic/fixed-trace/50%/90%/99% covariance, seeds and ablations collected | Column names/units/preprocessing unconfirmed; standardization changes the metric |
| Numerical correctness | Full small FP64 references, sampled large-input references, ties/scales/boundaries/segments and fixed-neighbor gradients collected | No universal FP32 certificate; million-point samples are not full-graph validation; learned/event inputs still missing |
| Matched approximate quality | CAGRA/GGNN latency and recall measured together on available inputs | These do not retroactively measure historical headline recall or replace learned/event comparisons |
| Complete-model cost | Not collected | CPU random-weight layer consistency is not trained-model GPU throughput, inference, or optimizer-step evidence |
| Peak memory | Independent NVML samples, baseline/absolute peak/delta and profiler passes collected; segmented FAISS repair passed | Sampling may miss brief peaks |
| Mechanism and smaller segments | Spectra, candidate/bin counters, stage profiles and synthetic segments collected | One-seed controls are not independently validated tuning; actual learned/event distributions missing |
| Novelty, limitations and reproducibility | Protocol, provenance and immutable returns available | Scientific interpretation, manuscript integration and original-review crosswalk still needed |
| H100 portability | Fresh CUDA 12.4/sm90 setup/build and 59 CPU tests passed | Actual H100 preflight, execution and timings absent |

## Measurement and repair record

First campaign: 41 cases / 421 successful bundles. Reverse extension:
63 cases / 668 planned bundles, ending at 654 successful, one failed and
13 missing. Every unresolved task is FAISS: 12 benchmarks including the
failed task, plus two profiles. Original records remain immutable.

The wrapper created a default FAISS scratch-resource object per segment;
64 objects could exceed the device's memory on a small segmented input.
The repair shares one resource across indexes queried serially on the same
device. It does not reduce requested neighbors or change the metric.
`repair.py` creates a new plan/run root and repeats every original backend
in affected cases, plus numerical gates. Repaired rows are not silently
inserted into the old plan or pooled across changed harnesses.

The repair completed all **152/152 bundles across 17 cases**, with zero
failed/missing bundles, in GPU job 64819 (10m43s). CPU job 64820 exported,
verified, imported and plotted the separate return. Reconciliation verifies
all 14 original FAISS gaps against unchanged task definitions, input hashes
and hardware identities. The original reverse return remains 654/668 with
its failure retained; no rows are rewritten or stitched across plans.
No GPU jobs remain queued. Total local full-A100 allocations across the
first campaign, reverse extension and repair were 8h32m10s.

Repair plan: `ee6135bac6fcb7b645f707a7e6a0068d215f76296d5e9daf5e8e9859e53b18f1`.
Private imported return: `Performance/revision_results/a100-faiss-repair-64820/`.
Reconciliation: `tmp/fgc-faiss-repair-20261111/reconciliation.json`.

## Replication and confidence intervals

New production timing bundles request one warmup and three measured
build-plus-query repetitions on each fixed input. Those measurements share
the input; they are not three independent datasets or fresh processes.
Main K=40 synthetic cells have three data seeds after the extension;
K=10/100 cells generally have two. Some ablations, equal-trace/50% controls,
segmented inputs and detector prefixes have only one independent input.

`analyze_results.py` writes `timing-repeatability.csv`, `seed-uncertainty.csv`
and `UNCERTAINTY.md`. Timing quartiles/ranges describe measurement variability.
Across-seed intervals use one paired median-time ratio per seed, take logs,
and apply a Student-t interval to their mean before exponentiating. Duplicate
input panels are collapsed. One-input cases have no across-input CI.
With only two or three seeds the normal-log-ratio assumption is weakly tested;
these are exploratory pointwise intervals, not proof of generalization or
absence of doubt. They do not include systematic protocol/hardware error.

FGC's check flag includes strict reference-distance checks. FAISS/cuVS/ANN
check flags enforce structural validity; some FAISS/cuVS raw-feature outputs
have less than full FP64-reference distance recall. Successful execution
must not be described as universal numerical agreement.

The original historical A100 campaign, the local reviewer campaigns and H100
results must retain their separate protocols and provenance. No reconstruction
accuracy, independent training runs or actual H100 timings follow from the
available local measurements.
