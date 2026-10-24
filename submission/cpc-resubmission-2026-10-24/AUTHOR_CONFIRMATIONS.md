# Author confirmations and evidence gaps

The manuscript contains no author-question placeholders. These flags are
separate from the submission PDF. They identify what the authors should
confirm or decide; unperformed experiments are not treated as completed work.

## Scientific claims and provenance

| ID | Claim or decision | Current wording and required resolution |
| --- | --- | --- |
| A1 | Connection to substantive HGCAL reconstruction | Sections 1 and 5.8 explain hit aggregation within shower reconstruction using published GravNet/object-condensation studies. Confirm that this describes the team's intended application. The paper does **not** establish improved shower separation, energy response, particle identification, or model throughput. Stronger claims require application measurements. |
| A2 | Identity and meaning of the HGCAL input | Confirm the source simulation, production/version, CMS access conditions, and the 1.16-billion-hit matrix provenance. Obtain the ten column definitions, units, and preprocessing from the data owner if possible. The current manuscript explicitly says these are unavailable; do not infer that the first three columns are physical positions. |
| A3 | Applicability to actual learned coordinates | The original GravNet four-coordinate example motivates the tested range; stored detector-feature prefixes are not learned embeddings. Confirm acceptance of this limited scope. Event-preserving learned-coordinate performance and end-to-end benefits require new data; they cannot be supplied by wording or author assent. |
| A4 | FP32 exactness | The theorem is in exact arithmetic. The unchanged released PCA tests use seeded Gaussian inputs up to N=8,000, with stated tolerances and segmented checks. Confirm that this is the intended numerical claim. No large-N detector-feature PCA correctness result or universal floating-point guarantee is asserted. Stronger claims require new validation or an error bound. |
| A5 | Approximate-backend comparisons | The 17x headline comparison is with timed CAGRA NN-Descent configurations whose recall was not measured. The archived recall table uses other configurations. Confirm this presentation; do not describe the headline result as matched-quality or infer its recall from the archive. |
| A6 | Parameter and distribution dependence | Binning dimension 3 is fastest at the documented d=8, N=5M, K=40 ablation cell. It is not established as universally optimal. Feature-prefix dimensionality, scales, covariance, and feature identity remain confounded in the detector study. New normalized/feature-controlled experiments would be needed to separate them. |
| A7 | Memory | The 5.15 GiB figure is a synchronized post-call NVML delta at d=3. Confirm that the resident-memory comparison is sufficient for the intended scope. It is not peak workspace or a peak-memory result for the d=8 PCA headline. |
| A8 | Novelty and attribution | The revision claims an implemented combination and its measured operating regime, not the invention of PCA indexing or contractive pruning. Confirm attribution relative to the cited thesis, upstream FastGraphCompute, and any overlapping preprint/publication. The revision creates no v1/v2 scientific narrative. |

## Submission decisions

- **Title and consent:** Approve the revised physics-facing title and the
  distinction between reconstruction motivation and detector-feature
  evidence. Confirm all authors approve the text and AI-use disclosure
  after reviewing this revision. Author order, emails, affiliations, and
  corresponding author were preserved, not independently reverified.
- **Journal route:** The pasted conversation describes an active Array
  revise-and-resubmit invitation. Confirm the actual status and intended
  venue; resolve any concurrent consideration before sending a new CPC
  submission. No journal action has been taken here.
- **CPC status:** The September 20 CPC decision welcomes a new paper; it is
  not a revision invitation under COMPHY-D-26-01041. The cover letter
  identifies that earlier submission without claiming an invited resubmission
  or guaranteed scope compliance.
- **Portal details:** Confirm current affiliations, any required ORCIDs,
  corresponding-author address, funding, competing-interest and contribution
  declarations, and the applicable article type before entering portal data.
  These have not been invented or certified by this editing pass.

The substantive decision is whether to submit the now more clearly scoped
kernel paper or first add application evidence. The original project scope
does not require new GPU work for this writing revision. That scope choice
does not guarantee that CPC will regard the existing stress test as adequate
physics validation.
