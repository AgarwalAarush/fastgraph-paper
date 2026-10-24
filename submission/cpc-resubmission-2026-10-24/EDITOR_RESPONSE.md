# Response to the September 20 CPC editorial comments

Draft for author review. References are to the revised manuscript. This
response concerns Andrew Hazel's decision on COMPHY-D-26-01041, not the
separate Array peer reviews.

**Connection to a substantive physics problem.**

We have rewritten the title, abstract, and Introduction around the separation
of overlapping showers in high-granularity calorimetry. Section 1 explains
the progression from measured hits to learned-coordinate neighbor graphs,
feature aggregation, and particle reconstruction, with references to
published HGCAL and GravNet studies. Section 5.8 describes precisely which
step FastGraph supplies within this chain. We distinguish that application
motivation from the existing evidence: the timing study uses concatenated
detector-feature inputs and does not establish reconstruction accuracy or
event-level throughput. Sections 6 and 8 state what remains to be measured.

**Accessible introduction and clear novelty and significance.**

Section 1 now introduces showers, pileup, hit graphs, and learned coordinates
before discussing search algorithms. It explains the cost of exhaustive
neighbor search and relates cell lists to computational methods familiar
from molecular simulation. The contribution is stated as a sampled-PCA
cell-list formulation and CUDA/PyTorch implementation retaining original-space
distance evaluation. Sections 1 and 2 acknowledge earlier PCA indexing and
spatial pruning, and separate the exact-arithmetic termination argument from
the finite-precision tests. The significance claimed is lower measured search
cost in a component relevant to graph-based calorimeter reconstruction.

**Scientific narrative and paragraph organization.**

We have replaced all 20 italicized run-in paragraph headings and the four
italic complexity labels with connected prose. The revised related-work
discussion moves from exhaustive search to spatial indices, projected
indexing, specialized three-dimensional methods, approximate search, and
their role in physics models. Methods, experimental setup, memory discussion,
and limitations now explain the relationships between choices and evidence.
The conclusion returns to the motivating reconstruction problem while
retaining the limits of the measured study.

**Extent of the revision.**

This is a substantive rewrite of framing and exposition, with tighter claims
and one detector-context reference. Author order and validated results are
preserved. No new event-batched timing, learned-embedding study, reconstruction
observable, matched-recall curve, peak-memory measurement, or large-scale
FP32 validation is represented as having been added.
