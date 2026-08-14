# Final Submission Review

## Executive verdict

**Ready with minor fixes, not blocked by additional experiments.** The
algorithmic argument, the final matched-input MPS:100 results, the main
figures, and the stated scope are coherent and professionally presented. Three
small but real manuscript corrections are required before calling the release
copy final: correct the replication statement, remove the nonexistent
appendix reference, and update the availability statement to name the existing
immutable release tags. No numerical result, central figure, citation key, or
layout defect was found that requires a new benchmark campaign.

## Mandatory fixes

1. **P1 -- Correct the number of timing repetitions.**
   [Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:661)
   says every backend has three repetitions per plotted cell. The checked-in
   final files instead contain seven repetitions for every one of 42 cells for
   FastGraph/PCA, FAISS, cuVS BF, and GGNN, and three for CAGRA NN-Descent:
   [gpu_matched_input_fgc_pca.csv](/home/export/aarusha/Performance/gpu_matched_input_fgc_pca.csv:1),
   [gpu_matched_input_faiss.csv](/home/export/aarusha/Performance/gpu_matched_input_faiss.csv:1),
   [gpu_matched_input_cuvs_bf.csv](/home/export/aarusha/Performance/gpu_matched_input_cuvs_bf.csv:1),
   [gpu_matched_input_ggnn.csv](/home/export/aarusha/Performance/gpu_matched_input_ggnn.csv:1), and
   [gpu_matched_input_cagra_nnd.csv](/home/export/aarusha/Performance/gpu_matched_input_cagra_nnd.csv:1).
   Say ``seven repetitions for FastGraph/PCA, FAISS, cuVS BF, and GGNN; three
   for CAGRA NN-Descent'' (or accurately state ``at least three'' and report
   the unequal counts). The plotted medians remain valid because
   [make_paper_plots_v4.py](/home/export/aarusha/FastGraph-Plotting/make_paper_plots_v4.py:89)
   groups and takes medians/IQRs.

2. **P1 -- Remove or repair the nonexistent appendix claim.**
   [Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:303) and
   [Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:1115) say
   that an object-condensation helper is ``described in the appendix,'' but
   the manuscript has no appendix. The source does contain an
   `ObjectCondensation` implementation
   ([object_condensation.py](/home/export/aarusha/FastGraphCompute-dev/fastgraphcompute/object_condensation.py:11)),
   so this need not become a code change. Remove the appendix wording; better,
   trim the unrelated helper from the abstract/keywords
   ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:182))
   and keep the paper focused on PCA-subspace exact kNN.

3. **P1 -- Make the availability statement match the release state.**
   [Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:1217)
   still says that an archive *will* pin the exact commits and characterizes
   the code URLs as moving. The immutable `pca-fgc-paper-v1.0.0` tags now pin
   the FastGraph source, performance data, plotting code, paper, and CLOVER
   fork; the submission README records that state
   ([README.md](/home/export/aarusha/Performance-Paper-PCA/README.md:41)).
   Replace the future-tense statement with the tag names/URLs and their commit
   identifiers. It is accurate to add that a GitHub Release/Zenodo DOI has not
   yet been minted. Do not promise public release of the CMS-restricted input.

## Recommended improvements

1. **P2 -- Tighten the scope signal in the abstract and keywords.** The
   object-condensation phrase and keyword are real library features but dilute
   the paper's much sharper contribution. The title and first two abstract
   sentences are already strong; keeping the abstract solely about the PCA
   kNN contribution will make the submission read more deliberate
   ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:170)).

2. **P2 -- Replace the slightly colloquial ``small-but-not-tiny'' phrasing.**
   ``Low-to-moderate-dimensional'' is the precise, consistent terminology
   used elsewhere and is stronger for a systems/scientific-computing venue
   ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:255)).
   This is stylistic, not an AI-authorship concern.

3. **P2 -- After the three text fixes, recompile and make one final page-image
   pass.** The current PDF has only a 1.9 pt output-routine overflow and
   bibliography underfull boxes; neither affects visible layout. Recompiling
   is simply needed so the final PDF and source agree.

## Verified strengths

- **Final numerical protocol is consistent.** The five matched-input CSVs
  contain exactly 1,302 successful rows and all use
  `preloaded_torch_cuda_zero_copy`: 294 rows each for FastGraph/PCA, FAISS,
  cuVS BF, and GGNN, and 126 for CAGRA NN-Descent. The source correctly
  describes a serialized `--gres=mps:100`, GPU-resident-input protocol that
  includes construction/search and excludes loading/H2D transfer
  ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:661)).
- **Headline claims trace cleanly.** The d=8, 5 M-point, k=40 medians are
  approximately 7.5 s (FastGraph/PCA), 310 s (FAISS), 146 s (cuVS BF), and
  127 s (CAGRA), producing the reported 41.23x, 19.41x, and 16.88x ratios
  ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:71)).
  The paper appropriately distinguishes exact FAISS/cuVS comparisons from
  approximate CAGRA/GGNN ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:735)).
- **Scope and limitations are unusually candid.** The manuscript correctly
  positions PCA's contribution at original d=4--10, retains d=2--3 as
  axis-aligned controls, and does not overextend detector-feature stress-test
  results to trained-model throughput
  ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:286),
  [Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:696),
  [Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:1167)).
- **Exactness presentation is sufficient for this empirical scope.** The
  contraction proof is clear and the tie-aware, brute-force checks are
  appropriately separated from the broader recall sweep
  ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:481),
  [Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:1056)).
- **Related work is adequate and balanced.** It covers exact GPU brute force,
  cell lists, PCA-indexing context, 3D-only RT/BVH methods, approximate GPU
  methods, and dynamic-graph GNNs
  ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:316)).
  All 34 cited bibliography keys resolve; no missing seminal citation was
  identified that would block submission. The direct CLOVER limitation is
  presented candidly rather than hidden
  ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:972)).

## Section-by-section summary

| Section | What it establishes | Review assessment |
|---|---|---|
| Abstract and Program Summary | Contribution, operational regime, software constraints | Clear and specific; trim the unrelated object-condensation material. |
| Introduction | Why dynamic exact kNN matters and why d=4--10 is the target regime | Strong logical funnel; explicitly avoids unsupported end-to-end claims. |
| Related Work | Position among exact, approximate, and 3D-only kNN systems | Broad, current enough, and fair to CLOVER/CAGRA. |
| Method | PCA subspace, full-space candidate distances, contraction proof, CUDA/PyTorch integration | Technically coherent; pseudocode and proof are well aligned. |
| Setup | Hardware, comparators, timing protocol, HGCAL/synthetic construction | Strong disclosure; correct the unequal repetition count. |
| Results | Headline dimensional scaling, size/k scaling, synthetic behavior, memory, ablation, CLOVER, recall | Numerically internally consistent and appropriately qualified. |
| Limitations | Feature scaling, distribution dependence, event batching, learned-latent gap, approximate-method tradeoff | Excellent restraint; reads like a serious scientific paper. |
| Availability and Conclusion | Reproduction path and final claim boundary | Update availability to the immutable tags; conclusion accurately preserves the limited claim. |

## Visual/layout check

The compiled [Paper.pdf](/home/export/aarusha/Performance-Paper-PCA/Paper.pdf)
is a 17-page A4 CPC-style manuscript. I rendered and inspected every page.
Figures are adjacent to the sections that interpret them; captions, tables,
the algorithm, code listing, equations, and references are placed
coherently. The headline table/plot pairing, multi-panel scaling figures,
and recall figure are legible at normal PDF zoom, with vector figures for
close inspection. No clipped figure, broken glyph, unresolved reference,
missing citation, bad float, accidental blank page, or overlapping text was
found. Fonts are embedded. The only TeX diagnostics are the previously noted
1.9 pt output overflow and bibliography underfull lines, which are not
visibly harmful.

## Reproducibility/data availability

The public Git state is already much stronger than the manuscript says:
the five repositories are pinned at `pca-fgc-paper-v1.0.0`, and the paper
tag matches its current `Paper.tex`, `Paper.pdf`, bibliography, and figures.
The README gives a credible reproduction path for the final matched-input
figures ([README.md](/home/export/aarusha/Performance-Paper-PCA/README.md:53)).
The raw HGCAL recHit features and correctness tensors are CMS-restricted and
should remain private; the manuscript's controlled-access description is
appropriate ([Paper.tex](/home/export/aarusha/Performance-Paper-PCA/Paper.tex:1237)).

There is no GitHub Release or Zenodo DOI yet. That is not a scientific-data
blocker, but the paper must not describe the existing tag-based archive as
future work. A DOI remains a useful final archival improvement after the
three mandatory wording fixes.

## Final verdict

**Ready with minor fixes.** There are **three P1 mandatory manuscript
corrections**, all narrow wording/provenance repairs. No further GPU jobs,
new HGCAL coordinate study, figure regeneration, bibliography expansion, or
algorithm/code change is required for this submission scope. The prose is
professional and technical rather than generically AI-like; its strongest
feature is the repeated, evidence-backed limitation of the claim rather than
unearned performance rhetoric.
