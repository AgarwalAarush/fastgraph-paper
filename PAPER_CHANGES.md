# PAPER_CHANGES.md — Pending v3 edit list

Living document. Update as items are landed or rescoped. Items are
grouped by paper section; the order at the bottom is the execution
order I'd follow.

Last sync: 2026-05-22 (after Binary A vs B 2x2 settled; CLOVER reframe
landed as v2; synth Binary A rerun queued as 15702).

---

## Status legend
- `[ ]` pending
- `[~]` in flight (data not yet landed)
- `[x]` done
- `[-]` skipped (with reason)

---

## A. Macros (top of file)

- [ ] A1. Update `\fgcVanillaBestDeight`: was `135\,s` (dev-binary mbd=6),
       should be `199.27\,s` (Binary A, axis best within released kernel
       surface 2-5, at mbd=2).
- [ ] A2. Update `\fgcVanillaBestPCAfactor`: was `18.8\ensuremath{\times}`,
       should be `26.6\ensuremath{\times}` (199.27 / 7.48).
- [~] A3. Bind `\spdSynthDthree` = `75\ensuremath{\times}` (vs FAISS, d=3 N=1M
       k=40 Gaussian). **WAIT** for synth Binary A rerun (job 15702) so
       the macros come from Binary A, not Binary B.
- [~] A4. Bind `\spdSynthDfive` = `8.6\ensuremath{\times}` (Binary A, same
       config). WAIT.
- [~] A5. Remove `\spdSynthDeight`, `\spdSynthDten` — PCA-FGC loses to
       cuVS BF at d>=6 on Gaussian. Use prose + small table instead.
       WAIT for Binary A confirmation of the crossover dimension.
- [ ] A6. Add `\onePassMBDoptPCA` = `7.48\,s` and `\onePassMBDoptAxis` =
       `199.27\,s` for the ablation section.

## B. Title / Abstract

- [ ] B7. Restrict any "faster than every backend" claim to "fastest
       exact GPU baseline". GGNN treated as approximate, separately.
       Grep for `every backend`, `faster than every`, `every other`.

## C. Introduction

- [ ] C8. Add Claim-1 paragraph (~150 words). Why exact kNN matters for
       HGCAL GNNs. Phrase training-nondeterminism + physics-systematic
       as motivation/risk, not proven pathology (no model study to
       cite).
- [ ] C9. Add d=4-10 latent-space framing (1-2 sentences). HEP-GNN
       dynamic graphs operate at d=4-10 in learned latent space (cite
       GravNet original + recent HGCAL multi-particle work). Currently
       only buried in sec:clover.
- [ ] C10. "Fastest exact GPU" restriction wherever it says "fastest"
       (parallel to B7).

## D. Related Work

- [ ] D11. Fix any "FAISS approximate" wording. `IndexFlatL2` is exact.
       Grep `\b(approximate)\b.*FAISS|FAISS.*approximate`.
- [x] D12. `\label{sec:related-work}` added in v1.

## E. Method (sec:method)

- [ ] E13. Add PCA short-circuit caveat in Phase 1: when `d <= k_bin`,
       the wrapper short-circuits to vanilla `binned_select_knn` — PCA
       contributes nothing at d=2,3,4 with default k_bin=3 (and at
       d=2,3 with k_bin=2). The d=2-4 HGCAL wins are inherited from
       the legacy cell-list method, not new contributions of this
       paper.

## F. Experimental Setup (sec:expsetup)

- [-] F14. Binary-discrepancy footnote NO LONGER NEEDED. Binary A
       ablation matches production headline (7.48 s vs 7.2 s) →
       same binary throughout, no footnote.
- [ ] F15. Cite the ablation CSVs explicitly: `ablation_binary_crosscheck.csv`
       (job 15555) and `ablation_max_bin_dims_binA.csv` (jobs 15555
       + 15578 combined).
- [-] F16. cuVS BF warm-up note. Skipped per Codex (low priority,
       median-of-3 already mitigates).

## G. Headline (sec:headline)

- [ ] G17. Add 1465x callout as one sentence framing the ablation
       transition. **Label clearly as internal PCA-vs-vanilla** (not
       external baseline). Template: "At small N and high d, vanilla
       axis-aligned falls into its brute-force fallback; e.g., at d=8
       N=10^5 k=40 the PCA path completes in 12\,ms vs.\ vanilla's
       16.93\,s, a 1465x internal speedup that motivates the ablation
       in Section sec:mbd-ablation."
- [ ] G18. Verify `tab:headline-speedups` caption does not include
       any "fastest, period" wording.

## H. Synthetic (sec:synthetic) — mandatory rewrite

- [~] H19. Replace current prose with the honest split (PCA-FGC wins
       at d <= 5 on Gaussian; cuVS BF wins at d >= 6 on isotropic
       data). WAIT for synth Binary A rerun (15702) so the dimension
       cutoff and exact ratios are from Binary A.
- [~] H20. Replace overclaim figures (currently say "FastGraph remains
       faster than the exact GPU baselines across d=2-10"). WAIT.
- [~] H21. Add small table at d=3, 5, 8 across the GPU baselines on
       Gaussian (instead of speedup macros for losing cells). WAIT.

## I. Memory

- [ ] I22. Verify measurement-caveat paragraph (added in v1) is still
       accurate and present.

## J. Ablation (sec:mbd-ablation) — replace table entirely

- [ ] J23. Replace dev-binary table with Binary A table at mbd in
       {2,3,4,5}:

       | mbd | axis (s) | PCA (s) | PCA speedup |
       |---|---|---|---|
       | 2 | 199.27 | 11.54 | 17.3x |
       | 3 | 204.65 | 7.48  | 27.4x ← PCA optimum |
       | 4 | 353.97 | 11.27 | 31.4x |
       | 5 | 242.90 | 28.10 | 8.6x  |

- [ ] J24. Drop mbd=6 row. Released kernel ships 2-5 only.
- [ ] J25. Update at-optima paragraph with the new ratio (26.6x).
- [ ] J26. Update U-shape narrative: PCA optimum at mbd=3, axis non-
       monotonic with minimum at mbd=2 within released range.

## K. Recall (sec:recall)

- [ ] K27. Add recall table with current CSV numbers, not stale NOTES:
       - FastGraph: recall_dist = 1.0 across tested configs
       - cuVS/CAGRA: mean ~0.73 at best/high-quality; 0.818 at
         d=3 N=500k k=40 representative cell
       - GGNN: mean ~0.666; catastrophic 0.40-0.57 at d=2-4
       - Neither approximate hits 99% at N >= 500k in tested rows
- [ ] K28. Delete any stale "FGC mean recall < 1.0" prose — that was
       the cdist-BLAS measurement artifact, resolved.

## L. CLOVER (sec:clover)

- [x] L29. Honest reframe with `tab:clover-d3` landed as v2 (commit
       6b4f566). No further changes needed.

## M. Conclusion

- [ ] M30. Add d=4-10 latent-space framing here too (currently only
       in CLOVER section).
- [ ] M31. Restrict "fastest" wording (parallel to B7).
- [ ] M32. Soften "data distribution no longer drives speedup" — synth
       and CLOVER prove distribution still matters. Replace with
       something like "FastGraph's PCA-subspace contribution is most
       effective on anisotropic data, where the principal components
       carry real structure."

## N. Data and Code Availability — rewrite

- [ ] N33. Honest version:
       - FastGraph public repo: `jkiesele/FastGraphCompute`
       - PCA branch / commit hash: TO BE RELEASED, exact hash once
         pushed. Currently on local `perf-fixes` branch in
         `FastGraphCompute-dev`; untracked remotely.
       - Benchmark scripts + data ledgers:
         `AgarwalAarush/fgc-performance`.
       - CMS HGCAL data: internal, CMS collaboration members only;
         external parties contact corresponding author.
       - CLOVER comparison: forked / patched from
         `ampslab/clover-knn` with local mods (k_values 30/128 -> 40,
         synthetic main path commented out, sm_80 build flags). Mods
         released with the paper as a fork or patch series.

## O. Limitations

- [ ] O34. Soften "data distribution no longer drives speedup" (same
       as M32 fix). Add: "PCA's effectiveness depends on data
       anisotropy; isotropic distributions reduce the gain to that
       of axis-aligned binning."

## P. Mechanical / build blockers

- [ ] P35. Bib merge from `Performance/references.bib`. Verify every
       `\cite{...}` in `Paper.tex` has a corresponding entry in
       `Performance-Paper-PCA/references.bib`. The agent-reconstructed
       bib may have wrong authors for some GPU-RT papers (flagged in
       the v1 commit message).
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
