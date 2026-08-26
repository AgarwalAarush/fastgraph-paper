# Editorial Manager Metadata

## Article

- Article type: Computational Physics Paper
- Title: FastGraph: PCA-Subspace Binned k-Nearest-Neighbor Graph Construction for GPU Geometric Deep Learning
- Running title: FastGraph PCA-Subspace Exact GPU kNN

## Keywords

Graph neural networks; k-nearest neighbors; GPU acceleration; CUDA; principal component analysis; particle physics

## Abstract

Dynamic graph neural networks repeatedly construct k-nearest-neighbor graphs
in learned latent spaces, making GPU-resident graph construction an important
operation in scientific point-cloud workloads. We extend FastGraph, a
PyTorch-integrated primitive for exact kNN graph construction in
low-to-moderate-dimensional learned spaces. The core contribution is a
PCA-subspace cell-list formulation: FastGraph fits a compact binning
coordinate system to the input coordinate tensor and uses that subspace for
spatial pruning, and evaluates all candidate distances in the original feature
space. This replaces the fixed coordinate-axis binning of the original
FastGraph method with a data-adaptive orthonormal subspace while preserving
exact neighbor sets, improving uniform-grid pruning in the d=4-10 regime
targeted by modern HGCAL reconstruction models. The implementation is
GPU-resident end to end and ships with an eager-mode PCA API, an opt-in
differentiable GravNetOp integration. On a 5 M-point CMS HGCAL recHit
workload, FastGraph builds the exact graph in 7.5 s at d=8, k=40, achieving
speedups of up to 41x over FAISS-GPU, 19x over cuVS brute force, and 17x over
approximate CAGRA while retaining exact neighbor sets under the paper's
distance-based convention.

## Authors

| Author | Affiliation | Email | Portal details still needed |
| --- | --- | --- | --- |
| Aarush Agarwal | Carnegie Mellon University, Pittsburgh, PA, USA | aarusha@andrew.cmu.edu | ORCID if available |
| Raymond He | Carnegie Mellon University, Pittsburgh, PA, USA | rhe2@andrew.cmu.edu | ORCID if available |
| Jan Kieseler | Karlsruhe Institute of Technology, Karlsruhe, Germany | jan.kieseler@cern.ch | ORCID if available |
| Matteo Cremonesi | Carnegie Mellon University, Pittsburgh, PA, USA | mcremone@andrew.cmu.edu | Corresponding author; postal address, phone, ORCID |
| Shah Rukh Qasim | University of Zurich, Zurich, Switzerland | shah.rukh.qasim@cern.ch | ORCID if available |

## Code And Data Availability

The FastGraph library, including the PCA-subspace extension described in this
paper, is publicly available at
https://github.com/AgarwalAarush/FastGraphCompute. The immutable
`pca-fgc-paper-v1.3.2` tags pin the exact library, benchmark harness,
plotting, manuscript, and CLOVER comparison-fork revisions used for this
submission. The public benchmark repository contains checked result CSVs,
figure-generation code, configurations, and seeded synthetic reproduction.
The CMS HGCAL recHit features are collaboration-restricted and cannot be
released; they are not required to reproduce the checked-in figures.

## Related Preprint

The manuscript cites the related original FastGraph preprint, arXiv:2511.10442
(2025). This submission presents the new PCA-subspace exact-kNN formulation,
its contraction-based exactness argument, an updated CUDA/PyTorch
implementation, and the matched-input A100 evaluation. Upload the preprint
only if Editorial Manager explicitly requests it.
