# Editorial Manager Metadata

## Article

- Article type: Computational Physics Paper
- Title: FastGraph: PCA-Subspace Binned k-Nearest-Neighbor Graph Construction for GPU Geometric Deep Learning
- Running title: FastGraph PCA-Subspace Exact GPU kNN

## Keywords

Graph neural networks; k-nearest neighbors; GPU acceleration; CUDA; principal component analysis; particle physics

## Abstract

Dynamic graph neural networks repeatedly construct k-nearest-neighbor graphs
in learned latent spaces, making GPU-accelerated graph construction an
important operation in scientific point-cloud workloads. We present
FastGraph, a PyTorch-integrated primitive for exact kNN graph construction in
low-to-moderate-dimensional spaces. FastGraph uses a PCA-subspace cell list:
it fits a compact binning coordinate system to the input tensor, uses that
subspace for spatial pruning, and evaluates all candidate distances in the
original feature space. The data-adaptive orthonormal subspace improves
uniform-grid pruning in the d=4-10 range evaluated around the d=4 GravNet
operating point. Point data remain GPU-resident, with small host
synchronizations for control metadata. The implementation ships with an
eager-mode PCA API and an opt-in differentiable GravNetOp integration. On a
5 M-point, single-segment detector-derived HGCAL recHit stress test, FastGraph
builds the exact graph in 7.5 s at d=8, k=40, achieving speedups of up to 41x
over FAISS-GPU, 19x over cuVS brute force, and 17x over approximate CAGRA while
retaining exact neighbor sets under the paper's distance-based convention.

## Authors

| Author | Affiliation | Email | Portal details still needed |
| --- | --- | --- | --- |
| Aarush Agarwal | Carnegie Mellon University, Pittsburgh, PA, USA | aarusha@andrew.cmu.edu | Corresponding author; postal address, phone, ORCID |
| Jan Kieseler | Karlsruhe Institute of Technology, Karlsruhe, Germany | jan.kieseler@cern.ch | ORCID if available |
| Raymond He | Carnegie Mellon University, Pittsburgh, PA, USA | rhe2@andrew.cmu.edu | ORCID if available |
| Matteo Cremonesi | Carnegie Mellon University, Pittsburgh, PA, USA | mcremone@andrew.cmu.edu | ORCID if available |
| Shah Rukh Qasim | University of Zurich, Zurich, Switzerland | shah.rukh.qasim@cern.ch | ORCID if available |

## Code And Data Availability

The FastGraph implementation described in this paper is publicly available at
https://github.com/AgarwalAarush/FastGraphCompute. The immutable
`pca-fgc-paper-v1.3.4` tags pin the exact library, benchmark harness,
plotting, manuscript, and CLOVER comparison-fork revisions used for this
submission. The public benchmark repository contains checked result CSVs,
figure-generation code, configurations, and seeded synthetic reproduction.
The CMS HGCAL recHit features are collaboration-restricted and cannot be
released; they are not required to reproduce the checked-in figures.

