# PAPER_CHANGES.md — Paper edit and submission-readiness list

Living document. Update as items are landed or rescoped. Items are
grouped by paper section; the order at the bottom is the execution
order I'd follow.

Last sync: 2026-07-24 (full PDF/source/release submission audit
completed; independent verifier agent findings integrated).

---

## Status legend
- `[ ]` pending
- `[~]` in flight (data not yet landed)
- `[x]` done
- `[-]` skipped (with reason)

---

## A. Macros (top of file)

- [x] A1. Update `\fgcVanillaBestDeight`: was `135\,s` (dev-binary mbd=6),
       should be `199.37\,s` (Binary A, axis best within released kernel
       surface 2-5, at mbd=2; median of 3 clean reps).
- [x] A2. Update `\fgcVanillaBestPCAfactor`: was `18.8\ensuremath{\times}`,
       should be `26.6\ensuremath{\times}` (199.37 / 7.48 = 26.65 → 26.6).
- [x] A3. Bound `\spdSynthDthree` = `55\ensuremath{\times}` (PCA-FGC vs
       cuVS BF, d=3 N=1M k=40 Gaussian, Binary A median of 3 reps).
       Anchor changed from FAISS to cuVS BF since cuVS BF is the
       fastest exact GPU baseline on isotropic data and "fastest exact
       GPU" is the paper's framing.
- [x] A4. Bound `\spdSynthDfive` = `4.8\ensuremath{\times}` (PCA-FGC vs
       cuVS BF, Binary A, same config).
- [x] A5. Removed `\spdSynthDeight` and `\spdSynthDten` — PCA-FGC loses
       to cuVS BF at d>=7 on Gaussian (crossover at d=7 on Binary A:
       PCA 7.8s, cuVS BF 6.6s). Replaced with `tab:synth-dim` table at
       d=3, 5, 7 in sec:synthetic (H21).
- [x] A6. Add `\onePassMBDoptPCA` = `7.48\,s` and `\onePassMBDoptAxis` =
       `199.27\,s` for the ablation section.

## B. Title / Abstract

- [x] B7. Restrict any "faster than every backend" claim to "fastest
       exact GPU baseline". GGNN treated as approximate, separately.
       Grep for `every backend`, `faster than every`, `every other`.

## C. Introduction

- [x] C8. Add Claim-1 paragraph (~150 words). Why exact kNN matters for
       HGCAL GNNs. Phrase training-nondeterminism + physics-systematic
       as motivation/risk, not proven pathology (no model study to
       cite).
- [x] C9. Add d=4-10 latent-space framing (1-2 sentences). HEP-GNN
       dynamic graphs operate at d=4-10 in learned latent space (cite
       GravNet original + recent HGCAL multi-particle work). Currently
       only buried in sec:clover.
- [x] C10. "Fastest exact GPU" restriction wherever it says "fastest"
       (parallel to B7).

## D. Related Work

- [x] D11. Fix any "FAISS approximate" wording. **Verified no occurrences
       in v2.** `grep -E 'approximate.*FAISS|FAISS.*approximate' Paper.tex`
       returns nothing; FAISS is consistently labeled "exact FAISS-GPU
       `IndexFlatL2`" at lines 174, 242, 566, 683.
- [x] D12. `\label{sec:related-work}` added in v1.

## E. Method (sec:method)

- [x] E13. Add PCA short-circuit caveat in Phase 1: when `d <= k_bin`,
       the wrapper short-circuits to vanilla `binned_select_knn` — PCA
       contributes nothing at d=2,3,4 with default k_bin=3 (and at
       d=2,3 with k_bin=2). The d=2-4 HGCAL wins are inherited from
       the legacy cell-list method, not new contributions of this
       paper.

## F. Experimental Setup (sec:expsetup)

- [-] F14. Binary-discrepancy footnote NO LONGER NEEDED. Binary A
       ablation matches production headline (7.48 s vs 7.2 s) →
       same binary throughout, no footnote.
- [x] F15. Cite the actual ablation CSVs on disk:
       - `Performance/ablation_binary_crosscheck.csv.contended_15553`
         (contains the d=8 N=5M k=40 mbd=3 and mbd=5 Binary A cells.
         The `.contended_15553` suffix marks that the first 3 reps at
         mbd=3 axis were collected under GPU contention from job 15553;
         only the last 3 reps at mbd=3 axis are clean. Methods footnote
         should explain this.)
       - `Performance/ablation_A_fill_24.csv` (mbd=2 and mbd=4 fill-in
         cells, Binary A, no contention).
       - `Performance/ablation_A_cuda13_crosscheck.csv` (the A-cuda13
         data point of the 2x2 toolchain experiment; informational
         only, not used in the paper headline).
- [-] F16. cuVS BF warm-up note. Skipped per Codex (low priority,
       median-of-3 already mitigates).

## G. Headline (sec:headline)

- [x] G17. Add 1465x callout as one sentence framing the ablation
       transition. **Label clearly as internal PCA-vs-vanilla** (not
       external baseline). Template: "At small N and high d, vanilla
       axis-aligned falls into its brute-force fallback; e.g., at d=8
       N=10^5 k=40 the PCA path completes in 12\,ms vs.\ vanilla's
       16.93\,s, a 1465x internal speedup that motivates the ablation
       in Section sec:mbd-ablation."
- [x] G18. Verify `tab:headline-speedups` caption does not include
       any "fastest, period" wording.

## H. Synthetic (sec:synthetic) — mandatory rewrite

- [x] H19. Synth prose replaced with honest split: PCA-FGC wins
       decisively at d=3, 5 (cell-list pruning dominates dense matmul);
       cuVS BF overtakes at d=7 (dense matmul near-optimal on
       isotropic data). Frames HGCAL d=6-10 wins as anisotropy result,
       not generic cell-list miracle. Added `\label{sec:limitations}`
       for the cross-reference.
- [x] H20. Old overclaim ("FastGraph remains faster than the exact GPU
       baselines across d=2-10") removed in v4.
- [x] H21. Added `tab:synth-dim` table at d=3, 5, 7 across PCA-FGC,
       cuVS BF, FAISS-GPU, CAGRA-nnd (median ms, Binary A).

## I. Memory

- [x] I22. Verify measurement-caveat paragraph (added in v1) is still
       accurate and present.

## J. Ablation (sec:mbd-ablation) — replace table entirely

- [x] J23. Replace dev-binary table with Binary A table at mbd in
       {2,3,4,5}. **Aggregator is median of clean reps** (n=3 per cell;
       contended reps at mbd=3 axis filtered out):

       | mbd | axis (s) | PCA (s) | PCA speedup |
       |---|---|---|---|
       | 2 | 199.37 | 11.39 | 17.5x |
       | 3 | 204.65 |  7.48 | 27.4x ← PCA optimum |
       | 4 | 353.78 | 11.58 | 30.6x |
       | 5 | 242.90 | 28.10 |  8.6x |

       (Earlier draft of this table mixed mean and median across
       mbd values. Median throughout is the safer aggregator given
       n=3 reps and the occasional outlier — e.g., pca mbd=3 has reps
       [7.17, 8.55, 7.48], where median 7.48 is more representative
       than mean 7.74.)

- [x] J24. Drop mbd=6 row. Released kernel ships 2-5 only.
- [x] J25. Update at-optima paragraph with the new ratio (26.6x).
- [x] J26. Update U-shape narrative: PCA optimum at mbd=3, axis non-
       monotonic with minimum at mbd=2 within released range.

## K. Recall (sec:recall)

- [x] K27. Add recall table with current CSV numbers, not stale NOTES:
       - FastGraph: recall_dist = 1.0 across tested configs
       - cuVS/CAGRA: mean ~0.73 at best/high-quality; 0.818 at
         d=3 N=500k k=40 representative cell
       - GGNN: mean ~0.666; catastrophic 0.40-0.57 at d=2-4
       - Neither approximate hits 99% at N >= 500k in tested rows
- [x] K28. Delete any stale "FGC mean recall < 1.0" prose — that was
       the cdist-BLAS measurement artifact, resolved.

## L. CLOVER (sec:clover)

- [x] L29. Honest reframe with `tab:clover-d3` landed as v2 (commit
       6b4f566). No further changes needed.

## M. Conclusion

- [x] M30. Add d=4-10 latent-space framing here too (currently only
       in CLOVER section).
- [x] M31. Restrict "fastest" wording (parallel to B7).
- [x] M32. Soften "data distribution no longer drives speedup" — synth
       and CLOVER prove distribution still matters. Replace with
       something like "FastGraph's PCA-subspace contribution is most
       effective on anisotropic data, where the principal components
       carry real structure."

## N. Data and Code Availability — rewrite

- [x] N33. Honest version (refined in v4 post-migration 2026-05-23):
       - FastGraph paper release: `AgarwalAarush/FastGraphCompute`
         (fork of `jkiesele/FastGraphCompute`), branch `paper-release`,
         tag `v1.0-paper` at commit `011d295`. Built with cuda 12.1
         toolchain (installed at `conda-envs/fgc-fast`).
       - Released kernel surface: k in {2, 3, 4, 5}. The mbd=6,7
         extension on local `perf-fixes` (commit `7cb5d1f`) is an
         ablation that confirmed mbd=7 hits a per-block register limit
         and is intentionally NOT published.
       - Benchmark scripts + data ledgers:
         `AgarwalAarush/fgc-performance`.
       - CMS HGCAL data: internal, CMS collaboration members only;
         external parties contact corresponding author.
       - CLOVER comparison: forked / patched from
         `ampslab/clover-knn` with local mods (k_values 30/128 -> 40,
         synthetic main path commented out, sm_80 build flags). Mods
         released with the paper as a fork or patch series.

## O. Limitations

- [x] O34. Soften "data distribution no longer drives speedup" (same
       as M32 fix). Add: "PCA's effectiveness depends on data
       anisotropy; isotropic distributions reduce the gain to that
       of axis-aligned binning."
- [x] O38. Added "Why exactness matters for the downstream GNN" paragraph
       after the "What still applies" block in sec:limitations. Frames
       exactness as a sensitivity-of-downstream argument rather than a
       raw-recall one: cites \cite{zugner2018adversarial} for GNN
       prediction shifts under structure-preserving edge perturbations
       and \cite{klicpera2019diffusion} for measurable downstream
       sensitivity to neighbourhood reweighting. Keeps the C8 honest
       framing (motivation/risk, not proven HEP pathology — explicitly
       disclaims that no model study was done). Both bib entries added
       to references.bib with DOI / arXiv pointers.
- [ ] O39. Add a brief mention of hybrid PCA-LBVH (or PCA-BVH) as a promising
       future direction to handle highly non-uniform data distributions with spatial
       occupancy skew, which uniform grid partitioning struggles to prune efficiently.

## P. Mechanical / build blockers

- [x] P35. Bib verification done for the 5 flagged GPU-RT papers
       (v4). Corrections applied:
       - `kamel2025clover`: Kamel/Yan/Chester authors corrected
         (Mahmoud->Victor, Da->Hanxueyu) per ICS '25 paper. DOI added.
       - `nagarajan2023arkade`: missing author Artem Pelenitsyn added,
         author order fixed (Mandarapu first per published paper).
         DOI added.
       - `evangelou2021rtknn`: entry metadata already correct
         (Nagarajan/Mandarapu/Kulkarni at ICS '23); citekey is
         misleading but a stable label, left as-is.
       - `wald2019rtnn`: entry metadata correct (Yuhao Zhu sole
         author, PPoPP '22); citekey misleading, left as-is.
       - `jakob2021optimized`: verified correct (Jakob & Guthe, CGF
         40(1):124-137, 2021).
- [ ] P36. Plot filenames (separate plotting track, not paper-text):
       - `gpu_fgc_dimensional_scaling_5M_k40_all_algorithms.png` —
         needs PCA-FGC curve + 5 backends
       - `gpu_fgc_speedup_d8_gpu.png` — NEW
       - `synth_dimensional_scaling_1M_k40_gpu.png` — NEW (wait for
         Binary A synth)
       - `synth_speedup_d3_gpu.png`, `synth_speedup_d8_gpu.png` —
         NEW (wait for Binary A synth)
       - `clover_headtohead_d3.png` — NEW
       - `memory_footprint.png`, recall plots, k-comparison — existing,
         regenerate with new data
- [~] P37. Top-up runs for full-grid std bars (job 15580 running,
       ~2-3 days). Not blocking paper text.

---

## Execution order (once Binary A synth lands)

1. Macros block (A1-A6) — mechanical, ~5 min.
2. Truth-issue prose (B7, C8-10, D11, H19-21, J23-26, K27-28, M30-32,
   N33, O34) — ~45 min.
3. Method + ablation + setup (E13, F15, G17-18) — ~20 min.
4. Mechanical fixes (P35) — ~15 min.
5. Single v3 commit.

Total estimated paper-text time: ~1.5h, after Binary A synth (job
15702) lands.

---

## Cross-reference status against NOTES.md

NOTES.md sections that map to v3 items:

| NOTES.md section | Paper item(s) |
|---|---|
| 2026-05-21 PCA-FGC results consolidated → Headline speedups | covered by v1 macros + tab:headline-speedups |
| 2026-05-21 max_bin_dims explanation | covered by E13 + sec:mbd-ablation (will be J23-J26 in v3) |
| 2026-05-21 memory-footprint fairness | covered by I22 (already in v1) |
| 2026-05-22 Binary A vs B 2x2 | drives A1-A6, J23-J26, F14 |
| 2026-05-22 CLOVER head-to-head | covered by v2 (L29 done) |
| 2026-05-22 Synth Gaussian cuVS BF wins at d>=6 | drives H19-H21 |
| 2026-05-22 Top-up queue | P37 (not blocking) |
| 2026-05-21 Paper positioning 3-claim | C8-C10, M30-M32 |
| 2026-05-21 Exactness evidence summary | already in v1 sec:exactness |

Anything in NOTES.md not yet mapped to a paper item → flag here:
- [ ] None currently flagged. Reaudit on each NOTES.md update.

---

## Q. Submission-readiness audit (2026-07-24)

Verdict: **not ready to submit as-is**. The exact-search method and
headline speedups remain promising, but the following items must be
resolved before submission. The current positioning should be
low-to-moderate-dimensional exact GPU kNN, with the new PCA regime at
`d=4--10`; retain `d=2--3` as inherited axis-aligned boundary controls.

### Q1. Submission blockers and explicitly deferred validation

- [>] Q40. Future work: make the benchmark event-aware. The current loader takes the
       first `N` rows of a flat 1.158B-hit array, and the runner creates
       `row_splits=[0,N]`; hits from many events are therefore treated as
       one graph and cross-event neighbours are permitted. Re-run with
       valid event boundaries, or state and justify the different task.
       Deferred by author decision on 2026-07-30; the paper labels the
       current measurement a single-segment detector-feature stress test.
- [>] Q41. Future work: validate the workload using actual learned latent
       coordinates from GravNet/HGCAL, preferably at
       `d={4,6,8,10}`. The current inputs are raw recHit feature columns,
       not trained latent embeddings, so the manuscript cannot yet claim
       end-to-end representativeness for dynamic-GNN latent-space kNN.
       Deferred by author decision on 2026-07-30; no end-to-end model
       throughput claim is made in this submission.
- [ ] Q42. Resolve venue and article type before the next formatting
       pass. The source targets Elsevier Computer Physics Communications
       (CPC), while project notes also mention ICML. The present
       16-page, named-author `elsarticle` manuscript is not an ICML
       submission. For CPC, decide Computational Physics vs Computer
       Programs in Physics (CPiP); CPiP requires a Program Summary and a
       complete distributable software package.
- [x] Q43. Correct the PCA API and integration claims. The paper's
       example passes positional argument `3` as `direction`, not
       `max_bin_dims`; the PCA wrapper is not `@torch.jit.script`; and
       released `GravNetOp` calls vanilla `binned_select_knn`, not the
       PCA wrapper. Implement and test the claimed integration or revise
       the text and example to match released code.
       Completed 2026-07-30: `GravNetOp` now exposes an opt-in
       `use_pca=True` eager path with dispatch and CUDA smoke coverage;
       the paper and README accurately preserve the scriptable
       axis-aligned default and describe PCA as eager-only.
- [ ] Q44. Publish a submission-grade immutable software artifact.
       Cite exact tag(s)/commit(s), add the advertised LICENSE file,
       document PCA installation/API usage, include a sample run and
       expected output, and add a CITATION/CFF plus archival DOI/PID.
       The README currently points installation at the upstream fork,
       says the paper is forthcoming, and advertises an absent license.
- [~] Q45. Reconcile the existing FastGraph preprint
       `arXiv:2511.10442`. If this manuscript supersedes it, upload a
       revised version; if it is a separate PCA contribution, cite it
       and clearly distinguish the prior axis-aligned FastGraph work.
       Do not submit with ambiguous overlap or a renewed "we introduce
       FastGraph" claim. The manuscript now cites and distinguishes the
       prior first-coordinate method; uploading a superseding arXiv
       version and disclosing it in the cover letter remain author actions.

### Q2. Experimental validity and reproducibility

- [ ] Q46. Document the recHit feature names, order, units, preprocessing,
       and normalization. Increasing `d` currently appends particular
       raw columns, so the `d=5` to `d=6` change may reflect feature
       identity/scale rather than dimensionality alone.
- [ ] Q47. Add standardized/whitened HGCAL controls and feature-order or
       subset controls. PCA on heterogeneous physical units is
       scale-sensitive; the current result may depend on the chosen
       units and column ordering.
- [~] Q48. Correct the PCA method description. Released code performs
       one global randomized `torch.pca_lowrank` projection from an
       unseeded 50k-point subsample, not a deterministic event-wise
       eigendecomposition. Either implement per-event deterministic PCA
       or disclose global fitting, subsampling, seed handling, and
       projection-variability measurements. Use centered
       `(X-mean)^T(X-mean)` in the mathematics.
       The global 50k-row subsample, `torch.pca_lowrank`, active PyTorch
       RNG state, and one-projection-per-call behavior are now disclosed;
       per-segment PCA and variability measurements remain pending.
- [x] Q49. Unify or accurately disclose the timing protocol. PCA and
       calibration runs used `mps:50`, while later CAGRA/GGNN runs used
       `mps:100`; the canonical CSVs merge allocations with a
       drift-aware policy. Prefer a clean canonical rerun under one
       allocation, otherwise document the merge and calibration.
       Completed 2026-07-30: archived Codex and Slurm records identify the
       later `mps:100` campaigns. All headline HGCAL plots now read only
       those clean files; legacy `mps:50` and exclusive rows are excluded.
- [~] Q50. Align timed regions across backends or quantify the
       difference. PCA-FGC receives GPU-resident data before timing,
       whereas FAISS/cuVS/CAGRA timing includes some host-to-device
       conversion and/or index setup.
       The asymmetry is now explicit: FastGraph/GGNN receive GPU-resident
       inputs while FAISS/cuVS/CAGRA include host-to-device transfer.
       A matched GPU-input rerun is queued under literal `mps:100` on
       2026-07-30: headline jobs 28964--28970 run first, followed by the
       remaining paper-grid jobs 28971--28975. Production depends on the
       five-backend zero-copy smoke chain 28959--28963.
- [x] Q51. Regenerate every headline scalar, table, and figure from one
       immutable aggregation. Current raw medians are approximately
       PCA-FGC 7.29 s, FAISS 307.19 s, cuVS 146.07 s, CAGRA 126.50 s,
       and GGNN 13.58 s at `N=5M,d=8,k=40`; several displayed rounded
       values/speedups derive from older inputs. Completed from the clean
       later sweeps, including vector figure regeneration.
- [x] Q52. Correct the memory caption/method. The instrumentation
       subtracts backend-specific output bytes (12 B for
       FastGraph/FAISS/cuVS, 8 B for CAGRA, 4 B for GGNN), not a common
       12 B per neighbour for every backend. Explain output-contract
       differences or normalize them. The paper now reports only the
       synchronized post-call NVML delta; unreliable Python-thread peak
       samples and derived workspace claims were removed.
- [x] Q53. Keep CAGRA's low-recall explanation observational unless a
       controlled normalization experiment isolates the cause. Add a
       normalization/metric ablation before recommending a mitigation
       as established fact. The causal diagnosis was removed.
- [~] Q54. Add a phase breakdown supporting "PCA estimation contributes
       negligibly," or weaken the claim. Add model-level profiling before
       claiming graph construction frequently dominates full model
       wall-clock. Unsupported model-bottleneck and negligible-PCA claims
       were removed; a phase breakdown/model profile would still add value.
- [~] Q55. Add end-to-end GravNet/model latency and physics-quality
       evidence, or narrow the title/abstract/conclusion to exact GPU
       kNN construction on detector data rather than geometric deep
       learning broadly. Claims are now narrowed to a detector-derived
       kernel stress test; end-to-end validation remains pending.
- [ ] Q56. Clarify the exactness proof/implementation correspondence:
       bins use one uniform scalar width across axes, and the stopping
       rule uses that width. The proof appears sound under the actual
       uniform-width implementation; avoid describing a different
       `wMin` construction without justification.

### Q3. Positioning and dimensional scope

- [x] Q57. Position the novel contribution at `d=4--10`, where
       `d>max_bin_dims=3`; keep `d=2--3` as controls showing continuity
       with released axis-aligned FastGraph. Do not describe `d=3` as
       part of the new PCA benefit, but do not remove it.
- [x] Q58. Narrow the application claim to GravNet/HGCAL-style
       low-to-moderate latent spaces unless higher-dimensional learned
       embeddings are evaluated. Remove the claim that ParticleNet and
       EdgeConv operate in the same `d=4--10` window; later dynamic-kNN
       layers commonly use much wider feature spaces.
- [ ] Q59. Do not launch a broad high-dimensional campaign yet. First
       obtain event-aware learned-latent and standardized controls. The
       existing `d=12` splice pilot can support an appendix only after
       its feature semantics are validated; the two `d=16` isotropic
       PCA points lack matching baselines and take about 19.5 min each.
       Collect real `d=16/32/64` data only if widening the paper beyond
       its low-dimensional positioning.
- [ ] Q59a. Curate the currently untracked high-dimensional CSV/log
       pilots in the Performance repository: either add a documented
       pilot-data manifest and intentionally exclude them from the paper,
       or integrate only validated results. Their present untracked state
       leaves the evaluation provenance ambiguous.
- [ ] Q60. Mention the completed PCA-LBVH study as future work, if useful:
       uniform-grid PCA wins in the realistic low-dimensional regime,
       while LBVH becomes competitive only near `d>=16` or under strong
       occupancy anisotropy. This also resolves pending item O39.

### Q4. Claims, related work, and references

- [x] Q61. Soften unsupported exactness motivation. The manuscript has
       no model study showing approximate neighbours preferentially
       remove boundary edges, create HGCAL physics systematics, or
       explain CMS's use of exact kNN. Keep these as plausible risks, or
       add direct evidence.
- [x] Q62. Replace Beyer et al. as the cell-list citation and add the
       original Verlet/cell-list literature plus a modern GPU
       neighbour-list reference (for example HOOMD-blue).
- [ ] Q63. Add formal versioned citations for cuVS and all major
       software/data artifacts, with DOI/PID where available. Cite
       foundational PCA/PCA-tree/random-projection work for the
       currently uncited method-history paragraph.
- [x] Q64. Correct bibliography metadata:
       `sproull1991refinements` is an Algorithmica journal article;
       the author of `bhattacharya2022gnn` is Saptaparna Bhattacharya;
       and `qasim2021multiparticle` has a published EPJ Web of
       Conferences version and DOI.
- [x] Q65. Audit newer exact GPU kNN/tree/grid work before claiming
       related-work coverage. Rephrase categorical statements such as
       LBVH/ray-tracing methods having "no defined extension" above 3D
       to the narrower claim actually supported by published
       implementations/evaluations.

### Q5. Writing, figures, and submission package

- [x] Q66. Fix the limitations statement that reduced PCA on isotropic
       data is "essentially a unitary rotation." For `k<d`, it is an
       arbitrary orthonormal `k`-dimensional projection.
- [ ] Q67. Decide whether the object-condensation helper appendix is
       essential. It currently has no evaluation and weakens the focus
       of a PCA-kNN paper; condense/remove it unless the CPC program
       article needs the broader library surface.
- [x] Q68. Export line/combo plots as vector PDF/EPS, enlarge panel text,
       legends, and axis labels, and supply figures as separate source
       files. Current 1600--3000 px PNG plots are below CPC's preferred
       full-page line-art guidance. All manuscript plots now have vector
       PDF outputs with embedded TrueType fonts and no Type 3 fonts.
- [ ] Q69. Reflow floats to reduce large blank regions on pages 9, 12,
       and 16 and avoid splitting the conclusion awkwardly. Resolve the
       remaining 1.9 pt overfull box.
- [x] Q70. Standardize US/British spelling, punctuation around paragraph
       headings, terminology, and capitalization. Enable working
       hyperlinks if allowed by the selected template.
- [ ] Q71. Complete the venue checklist: Program Summary if CPiP,
       funding statement, competing-interest declaration, author
       contributions, data/code availability, corresponding-author
       details, separate artwork, source archive, and any required
       highlights.

### Q6. Verified clean items

- [x] Q72. PDF builds to 18 A4 pages with embedded/subset fonts, no Type
       3 fonts, and no undefined citations/references. A 1.9 pt
       class-level output-box overflow and bibliography underfull notices
       remain visually benign.
- [x] Q73. The PCA contraction plus shell-termination exactness argument
       is consistent with the released uniform-bin-width implementation;
       no proof-breaking issue was found in this audit.
- [x] Q74. Source-to-PDF freshness is verified for the audited artifact:
       `Paper.pdf` was regenerated on 2026-07-30 after the latest
       manuscript, bibliography, and vector-figure edits.

### Q7. Second verifier pass (2026-07-30)

- [x] Q75. Correct recall provenance. The archived broad recall CSV uses
       the axis kernel and is labeled accordingly. A dedicated PCA-wrapper
       verifier passed at `d={4,5,8,10}`, `K={16,40,128}`, random PCA
       subsampling, and multi-segment row splits against FP32 brute force.
- [x] Q76. Match the bin-count description to the released code's
       historical occupancy proxy. This heuristic affects performance,
       not the exactness condition; changing it would require retiming.
- [x] Q77. Replace the full-eigendecomposition complexity claim with the
       sampled randomized low-rank fit plus `O(Ndk)` projection cost.
- [x] Q78. Disclose the deterministic first-row/first-column feature-prefix
       protocol and remove the causal claim that the `d=5` to `d=6` jump
       isolates dimensionality or PCA anisotropy. Controls remain Q46-Q47.
- [x] Q79. Add CPC Program Summary and highlights; add MIT `LICENSE` and
       `CITATION.cff` to the software package. Immutable archive/DOI and
       author declarations remain Q44/Q71.
