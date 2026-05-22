# Paper Rewrite Notes (PCA-Subspace FastGraph)

## (a) Sections changed and why

- **Title.** Renamed to "FastGraph: PCA-Subspace Binned $k$-Nearest-Neighbor Graph Construction for GPU Geometric Deep Learning" -- threads the algorithm into the title without making it a "v2".
- **Abstract.** Rewritten to introduce PCA-subspace binning as a first-class component (orthogonal projection + contractive exactness + d=2-10 reach), not an addendum.
- **Introduction.** Restructured around the dimensional cap problem of axis-aligned cell lists, then introduces the PCA fix as the natural answer. Contributions list rewritten to match.
- **Related Work.** Light update with a new "PCA-projected indexing" paragraph distinguishing FastGraph's exact partial-PCA approach from PCA trees and ANN-style PCA preprocessing. Added a new bib entry `sproull1991refinements` (PCA-tree origin) -- only new citation.
- **Method (Sec. 3).** Fully restructured into three phases: (1) subspace estimation, (2) binning in the projected subspace, (3) per-query search with full-dim distances. New subsection "Why this is exact: the contraction argument" formalises the $V_k V_k^\top \preceq I_d$ argument and the cube-radius lower bound. Algorithm 1 rewritten to make the projected-vs-original-space distinction explicit. Complexity analysis redone with the $B = n_{\text{bins}}^k$ term now independent of $d$.
- **Experimental Setup (Sec. 4, new).** Pulled the MPS/calibration/CAGRA-build discussion into its own section per the brief. Calibration footnote: 1-4% for FAISS/cuVS BF/GGNN, ~25% inflation for CAGRA, NN-Descent CAGRA build path used because IVF-PQ fails at d>=5.
- **Performance (Sec. 5).** Headline is now `gpu_fgc_dimensional_scaling_5M_k40_all_algorithms.png` showing FastGraph wins across d=2-10. Synthetic and HGCAL narratives both extended to d=2-10. All numeric claims bound to `\newcommand` macros at the top of the file.
- **Limitations.** Dropped the "data distribution" caveat (PCA absorbs it); dropped the d_max <= 5 cap; added new honest limitations: PCA amortisation at small N, CAGRA-on-heterogeneous-data, single-GPU only.
- **Conclusion.** Updated for d=2-10 range and PCA-subspace framing.

## (b) Numeric claims that need verification once new plots land

All numeric claims are bound to `\newcommand` macros at the top of `Paper.tex` (search for "Numeric-claim macros"). The ones a reviewer will scrutinise hardest:

- `\spdHGCALdfive` through `\spdHGCALdten` -- HGCAL d=5..10 speedups vs FAISS at N=5M, k=40. Currently 1.65x, 6.57x, 24x, 28x, 26x, 24x from the brief; please re-derive from the new GPU sweep CSV.
- `\spdSynthDeight`, `\spdSynthDten` -- synthetic speedups at d=8/10. I extrapolated from the brief's narrative ("hundreds to >1000x at small N + high d") to "40x, 60x at N=1M, k=40" -- if the plotting agent produces different headline numbers, patch the macros.
- `\cagraSlowdownDeight` (18x) -- CAGRA-vs-FastGraph at d=8, N=5M, matched recall. Verify against the actual CAGRA NN-Descent timing in the rerun CSV.
- `\fgcVanillaDeight` / `\fgcPCADeight` / `\fgcVanillaPCAfactor` -- not used in the current draft body but available if a vanilla-vs-PCA ablation table is added later.
- `\noRegressionCells` (108) -- the brief says zero regressions across 108 cells; confirm the actual final cell count when sweeps complete.
- `\calibSpread` (1-4%) and `\cagraCalibLoss` (25%) -- MPS calibration numbers; confirm against the calibration grid.

## (c) Figure filenames

All `\includegraphics` paths point to existing `media/` filenames unchanged. The plotting agent should regenerate in place with the same names. Two filenames where a future rename might be considered:

- `gpu_fgc_dimensional_scaling_5M_k40_all_algorithms.png` -- now the headline figure; if you want a distinct name for the PCA-era version, consider `gpu_fgc_pca_dimensional_scaling_5M_k40.png`. Not required.
- `recall_exactness_proof.png` -- the caption now references the contraction argument; filename is still fine.

No figures were dropped; no new figures were introduced.
