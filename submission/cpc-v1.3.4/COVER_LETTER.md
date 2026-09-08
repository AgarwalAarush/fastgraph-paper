[Date]

Dear Editors of *Computer Physics Communications*,

Please consider our manuscript, “FastGraph: PCA-Subspace Binned
k-Nearest-Neighbor Graph Construction for GPU Geometric Deep Learning,” as a
Computational Physics Paper.

The manuscript introduces a PCA-subspace cell-list formulation for exact GPU
k-nearest-neighbor graph construction. It uses a compact principal-component
subspace only for spatial pruning while retaining full-dimensional candidate
distance evaluation; a contraction argument establishes exactness. The
released CUDA/PyTorch implementation is evaluated on a matched-input,
serialized A100 study using CMS HGCAL recHit features, where it substantially
outperforms the tested exact GPU baselines in the stated low-to-moderate
dimensional regime.

The contribution is appropriate for CPC because it combines a new
computational method, its GPU implementation, reproducible public benchmark
artifacts, and a substantive particle-physics workload. The exact source,
benchmark harness, plotting workflow, and manuscript are pinned by immutable
`pca-fgc-paper-v1.3.4` tags. Restricted CMS inputs are clearly identified;
public result inputs and seeded synthetic reproduction are available.

This manuscript is not under consideration elsewhere.

[AUTHOR CONFIRMATION REQUIRED: All authors have approved the manuscript and
agree to its submission to *Computer Physics Communications*.]

Sincerely,

Aarush Agarwal
Corresponding author
[postal address]
[telephone number]
aarusha@andrew.cmu.edu
