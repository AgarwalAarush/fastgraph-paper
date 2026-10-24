# Cover-letter draft — author review required

October 24, 2026

Dear Professor Hazel and Editors of *Computer Physics Communications*,

Please consider “FastGraph: PCA-Subspace Binning for Exact GPU Neighbor
Search in Calorimeter Reconstruction” as a Computational Physics Paper.
We have substantially rewritten the presentation following the September 20
editorial decision on COMPHY-D-26-01041 and your indication that a new paper
addressing the concerns would be welcome.

The manuscript now begins with the physics problem of separating overlapping
calorimeter showers and explains how repeated neighbor search enters
GravNet-based hit reconstruction. It presents a sampled-PCA cell-list search
with full-coordinate distance evaluation and a CUDA/PyTorch implementation.
The Introduction addresses a general computational-physics audience, and the
report-style italicized mini-sections have been replaced by a connected
scientific narrative.

The measured contribution is acceleration of neighbor construction on stated
HGCAL detector-feature stress tests, supported by synthetic controls and
implementation tests. We explicitly distinguish those results from
event-batched learned-coordinate graphs, reconstruction observables, and
complete-model throughput, which have not been measured here. The rewritten
paper does not claim that a kernel speedup alone demonstrates better physics
performance. The accompanying response maps each editorial concern to the
revised text, and the experimental artifacts retain their existing immutable
release identity.

[BEFORE SENDING: resolve the separate Array submission status and insert
truthful declarations about exclusive consideration, all-author approval,
and any other required disclosures. See AUTHOR_CONFIRMATIONS.md.]

Sincerely,

Aarush Agarwal  
Corresponding author  
aarusha@andrew.cmu.edu
