# Proposed CPC portal metadata

Author-review copy; no portal entries have been changed.

- Article type: Computational Physics Paper (confirm at submission).
- Title: FastGraph: PCA-Subspace Binning for Exact GPU Neighbor Search in Calorimeter Reconstruction
- Running title: FastGraph GPU Neighbor Search for Calorimeter Reconstruction
- Keywords: Calorimeter reconstruction; computational particle physics;
  k-nearest neighbors; GPU computing; principal component analysis;
  graph neural networks.

## Abstract

Separating overlapping particle showers in the CMS High Granularity
Calorimeter (HGCAL) requires reconstruction methods that exploit sparse,
irregular energy deposits. GravNet-based approaches exchange information
between hits through neighbor graphs in learned coordinate spaces, requiring
repeated graph construction. We present FastGraph, a CUDA/PyTorch
implementation of exact k-nearest-neighbor search motivated by this
computational task. It uses a principal component analysis (PCA) subspace
for cell-list pruning while evaluating candidate distances in the original
feature space. An orthonormal projection supplies a lower bound for exact
search in exact arithmetic; finite-precision correctness is assessed
separately in bounded tests. The study covers d=2–10, with PCA used at
d=4–10, and includes an opt-in differentiable GravNet integration. On a
5 M-point, single-segment HGCAL detector-feature stress test at d=8, k=40,
FastGraph constructs the graph in 7.5 s, with speedups of up to 41x over
FAISS-GPU and 19x over cuVS brute force. The measured speedup over
approximate CAGRA is 17x, without a matched-recall comparison. These results
establish a kernel-level advantage on the tested detector-feature
distributions; event-batched learned-coordinate workloads, reconstruction
performance, and end-to-end model throughput remain to be evaluated.

## Authors in preserved order

| Author | Affiliation | Email |
| --- | --- | --- |
| Aarush Agarwal | Carnegie Mellon University, Pittsburgh, PA, USA | aarusha@andrew.cmu.edu |
| Jan Kieseler | Karlsruhe Institute of Technology, Karlsruhe, Germany | jan.kieseler@cern.ch |
| Raymond He | Carnegie Mellon University, Pittsburgh, PA, USA | rhe2@andrew.cmu.edu |
| Matteo Cremonesi | Carnegie Mellon University, Pittsburgh, PA, USA | mcremone@andrew.cmu.edu |
| Shah Rukh Qasim | University of Zurich, Zürich, Switzerland | shah.rukh.qasim@cern.ch |

Aarush Agarwal remains the sole corresponding author. Confirm affiliations,
required identifiers, contact details, and all-author approval before use.

## Availability and declarations

Use the manuscript's Data and Code Availability Statement. Experimental
artifacts remain pinned by `pca-fgc-paper-v1.3.4`; that tag is not the new
manuscript revision. The HGCAL input is CMS-restricted, and feature semantics
and event boundaries are unavailable in the supplied artifact. Public result
inputs and seeded synthetic reproduction remain available through the cited
repositories.

Preserve and review the manuscript's generative-AI disclosure. Exclusive
consideration, author approval, funding, contributions, and competing-interest
declarations require author input; the historical declarations are not
automatically certified for this proposed submission.
