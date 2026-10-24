# CPC manuscript revision — October 24, 2026

## Basis and scope

Revised `Paper.tex` from clean baseline commit
`9cc296df1bb4e97b97c5ddf4c025fe47b0936fb7` (the October 22 arXiv
presentation). The controlling editorial source is Andrew Hazel's
[September 20 decision on COMPHY-D-26-01041](https://mail.google.com/mail/u/?authuser=aarusha%40andrew.cmu.edu#all/1a0bf44d7a726ac0),
read directly for this revision. The editor declined external review but
welcomed a new paper addressing the stated concerns. This is a proposed new
CPC submission, not an invited revision of the rejected manuscript number.

The pasted conversation concerns the separate October Array reviews. It was
used to identify claims requiring care, not as the source of CPC's decision
or as evidence that any requested experiments have been completed.

## Editorial changes

| CPC concern | Revision | Manuscript location |
| --- | --- | --- |
| Substantive physics connection is unclear | Retitled the paper around calorimeter reconstruction; introduced overlapping showers, pileup, hit assignment, and particle-property estimation before the search algorithm. | Title, abstract, Section 1 |
| Introduction assumes a specialist computing audience | Defined hits, graphs, learned coordinates, and the role of neighbor aggregation; connected cell lists to molecular simulation and explained why a full grid is expensive. | Section 1 |
| Novelty and significance need articulation | Described the contribution as sampled-PCA cell-list search with full-space distances and a CUDA/PyTorch realization; explicitly recognized established PCA indexing and lower-bound pruning. | Sections 1–3 |
| Report-like italicized mini-sections lack continuity | Replaced all 20 `paragraph*` headings and four italic complexity labels with connected paragraphs. Added transitions between related-work families, setup choices, results, and limitations. Combined the shell-enumerator and pseudocode discussions. | Sections 1–6 |
| Physics relevance must be supported accurately | Added a reconstruction-chain discussion explaining that neighbor edges support feature aggregation rather than directly assign showers. Distinguished motivating application, integration capability, and measured kernel performance. | Abstract, Sections 1, 5.8, 6, 8 |

Added a detector-context reference to Florian Pitters, *The CMS
High-Granularity Calorimeter for Operation at the High-Luminosity LHC*,
[arXiv:1802.05987](https://arxiv.org/abs/1802.05987). The reconstruction
explanation was checked against the primary
[GravNet paper](https://doi.org/10.1140/epjc/s10052-019-7113-9) and
[multi-particle HGCAL study](https://arxiv.org/html/2106.01832), both already
cited in the manuscript. No detector channel count, collision rate, or
timing improvement beyond the existing results was added.

## Claim corrections

- Removed the abstract's implication that exact neighbor sets were validated
  at the 5M-point PCA timing configuration. Retained the exact-arithmetic
  argument and reported finite FP32 tests separately.
- Identified the 17x CAGRA result as an unmatched-recall timing comparison in
  the abstract and conclusion, consistent with the existing results section.
- Removed suggestions that exact search alone controls physics systematics
  or establishes reproducible graphs or gradients.
- Restricted the conclusion to tested detector-feature distributions;
  removed the prediction of general usefulness across scientific GNNs.
- Replaced unmeasured claims about which intrinsic dimensions prefer binning
  sizes 4 or 5 and about very small events always preferring axis-aligned
  search with explicit tradeoffs requiring measurement.
- Qualified column-permutation invariance for a sampled FP32 PCA fit and
  removed unsupported descriptions of uniform-grid or BLAS optimality.
- Retained unknown feature semantics, changing feature prefixes, missing
  event-preserving timings, missing learned embeddings, and post-call rather
  than peak memory as disclosed limitations.

## Preserved experimental record

The author order remains Aarush Agarwal, Jan Kieseler, Raymond He, Matteo
Cremonesi, Shah Rukh Qasim. Aarush remains the sole corresponding author.
Affiliations and emails are unchanged.

A source comparison against the baseline verified byte-for-byte preservation
of all numeric-claim macros, every figure block and caption, every table,
the algorithm, the usage listing, the exactness proof, the complete recall
protocol and PCA validation account, and the availability statement. Figure
assets and benchmark artifacts were not modified. In particular, the 7.5 s,
41.23x/19.41x/16.88x reference-cell results, 26.6x internal ablation ratio,
recall values, replication counts, and numerical tolerances remain intact.

No benchmarks, model training, GPU allocations, or new correctness experiments
were run. The existing `pca-fgc-paper-v1.3.4` experimental tags and historical
Array/arXiv submission archives remain unchanged.

## Deliverables and remaining decisions

The active source and PDF are `Paper.tex` and `Paper.pdf`. This directory
contains the proposed CPC source archive, a matching PDF, updated submission
metadata, an editor-response draft, a cover-letter draft, and
`AUTHOR_CONFIRMATIONS.md`. The flags distinguish author-verifiable provenance
from claims that require new measurements; confirmation alone cannot supply
missing experimental evidence.

The manuscript now addresses the requested framing and narrative changes.
Whether the present kernel study supplies sufficient physics-context evidence
for CPC remains an editorial judgment. The author flags must be resolved
before an actual submission, particularly the separate Array consideration.
