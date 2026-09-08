# CPC Portal Entry Guide

Target journal: *Computer Physics Communications* (CPC)

Article type: **Computational Physics Paper**

Official portal: https://www.editorialmanager.com/comphy/default2.aspx

Prepared from the CPC Guide for Authors and the live CPC Editorial Manager
entry page on 2026-08-23. Editorial Manager shows its final set of questions
only after the corresponding author signs in, so journal-configured questions
may appear in addition to the standard flow below.

## Resolve Before Opening A New Submission

- **Aarush Agarwal email:** `aarusha@andrew.cmu.edu`.
- Confirm the corresponding author is Aarush Agarwal and has an Elsevier
  account or ORCID login.
- Confirm all five authors approve the final manuscript, author order, and
  CPC submission.
- Confirm the competing-interest, funding, CRediT, and generative-AI wording
  in `AUTHOR_DECLARATIONS.md`.

## Fast Submission Order

1. Sign in with the authorized submitter's Elsevier account. Aarush Agarwal
   must have a registered Editorial Manager record because he is the
   corresponding author.
2. Select **Submit New Manuscript** and then select article type
   **Computational Physics Paper**.
3. Upload the source bundle first and designate it **Manuscript**:
   `/home/export/aarusha/tmp/FastGraph-CPC-CP-v1.3.4-source.zip`
4. Add `highlights.txt` as **Highlights**.
5. Add the cover letter if the portal provides a Cover Letter file type;
   otherwise paste its text into the Comments to the Editor field.
6. Complete the metadata below, check the generated PDF, and submit.

Do not upload the restricted HGCAL input data, the private correctness
tensors, a CPiP Program Summary, or a CPC Program Library archive. This is a
Computational Physics Paper, not a Computer Programs in Physics submission.

## Article Metadata

### Title

```text
FastGraph: PCA-Subspace Binned k-Nearest-Neighbor Graph Construction for GPU Geometric Deep Learning
```

### Short or Running Title

Enter only if Editorial Manager presents this field:

```text
FastGraph PCA-Subspace Exact GPU kNN
```

### Abstract

```text
Dynamic graph neural networks repeatedly construct k-nearest-neighbor graphs in learned latent spaces, making GPU-accelerated graph construction an important operation in scientific point-cloud workloads. We present FastGraph, a PyTorch-integrated primitive for exact kNN graph construction in low-to-moderate-dimensional spaces. FastGraph uses a PCA-subspace cell list: it fits a compact binning coordinate system to the input tensor, uses that subspace for spatial pruning, and evaluates all candidate distances in the original feature space. The data-adaptive orthonormal subspace improves uniform-grid pruning in the d=4-10 range evaluated around the d=4 GravNet operating point. Point data remain GPU-resident, with small host synchronizations for control metadata. The implementation ships with an eager-mode PCA API and an opt-in differentiable GravNetOp integration. On a 5 M-point, single-segment detector-derived HGCAL recHit stress test, FastGraph builds the exact graph in 7.5 s at d=8, k=40, achieving speedups of up to 41x over FAISS-GPU, 19x over cuVS brute force, and 17x over approximate CAGRA while retaining exact neighbor sets under the paper's distance-based convention.
```

### Keywords

Enter as separate keywords if the portal uses separate boxes:

```text
Graph neural networks
k-nearest neighbors
GPU acceleration
CUDA
principal component analysis
particle physics
```

### Classification

Only select classifications that are actually offered by the portal. Prefer
the closest available choices for computational methods/algorithms, GPU or
high-performance computing, scientific software, and particle physics. Do
not invent a classification or choose an unrelated discipline just to fill a
non-mandatory field.

## Author List

Enter the authors in this exact order. The corresponding-author checkbox is
on Aarush Agarwal only.

| Order | Given name | Family name | Email | Affiliation | Corresponding |
| --- | --- | --- | --- | --- | --- |
| 1 | Aarush | Agarwal | aarusha@andrew.cmu.edu | Carnegie Mellon University, Pittsburgh, PA, USA | Yes |
| 2 | Jan | Kieseler | jan.kieseler@cern.ch | Karlsruhe Institute of Technology, Karlsruhe, Germany | No |
| 3 | Raymond | He | rhe2@andrew.cmu.edu | Carnegie Mellon University, Pittsburgh, PA, USA | No |
| 4 | Matteo | Cremonesi | mcremone@andrew.cmu.edu | Carnegie Mellon University, Pittsburgh, PA, USA | No |
| 5 | Shah Rukh | Qasim | shah.rukh.qasim@cern.ch | University of Zurich, Zurich, Switzerland | No |

Enter ORCIDs if the relevant author confirms one. Do not guess or create one.
For Aarush, use the postal address and telephone number that he confirms in
his author profile if the portal requests contact details.

## Standard Editorial Manager Steps

Editorial Manager's normal order is Article Type Selection, Attach Files,
General Information, Review Preferences, Additional Information, Comments,
and Manuscript Data. CPC may add, remove, or reorder questions.

### Attach Files

| Portal item type | File or text | Entry |
| --- | --- | --- |
| Manuscript | Source archive | `/home/export/aarusha/tmp/FastGraph-CPC-CP-v1.3.4-source.zip` |
| Highlights | Editable text file | `highlights.txt` |
| Cover Letter | If offered | `COVER_LETTER.md`, after its placeholders are confirmed |
| Competing Interest Declaration | Only if the portal requires a file/template | Complete the CPC template with the confirmed declaration |
| PDF | Only if explicitly requested | `Paper.pdf` |

The source archive was checked with `unzip -t`; its SHA-256 is
`b560885dfce29e74bd0968501b648e5efc718b8c8b7ad79b924f44d886b61ec2`.
Do not add figures one by one unless the portal rejects the source archive.

### General Information

Use the title, running title, abstract, and keywords above. If the portal
asks whether this is a resubmission or transfer, answer **No**. This is a new
CPC submission, and it is not under consideration elsewhere.

### Review Preferences

Do not enter unverified suggested reviewers or exclusions. If CPC makes
reviewer suggestions mandatory, choose qualified experts with no recent
collaboration, institutional overlap, or other conflict, then record each
name, institution, email, and conflict rationale before submission. Get
corresponding-author approval for the final list.

### Additional Information And Declarations

Use only after the corresponding author confirms the statements in
`AUTHOR_DECLARATIONS.md`.

**Competing interests, if none:**

```text
The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
```

**Funding, if none:**

```text
This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.
```

**Generative-AI disclosure, if asked and approved:**

```text
During the preparation of this work, the authors used OpenAI Codex for language editing, software review, and reproducibility checks. The authors reviewed and edited the output as needed and take full responsibility for the content of the published article.
```

**Data and code availability:**

```text
The FastGraph implementation described in this paper is publicly available at https://github.com/AgarwalAarush/FastGraphCompute. The immutable pca-fgc-paper-v1.3.4 tags pin the exact library, benchmark harness, plotting, manuscript, and CLOVER comparison-fork revisions used for this submission. The public benchmark repository contains checked result CSVs, figure-generation code, configurations, and seeded synthetic reproduction. The CMS HGCAL recHit features are collaboration-restricted and cannot be released; they are not required to reproduce the checked-in figures.
```


If the portal asks whether the manuscript is currently under consideration
elsewhere, answer **No**. Answer any prior-publication question truthfully
using the authors' confirmed submission history.

### Comments To The Editor

Paste the body of `COVER_LETTER.md` after replacing the author-confirmation
placeholder, postal address, and telephone number. Include the reproducibility
statement.

### Manuscript Data

Verify every extracted or entered value against this guide and the manuscript:

- article type is **Computational Physics Paper**;
- author order and corresponding author match the table above;
- title and abstract match exactly;
- all six keywords are present;
- affiliations are correctly linked to authors;
- public repositories use the immutable `pca-fgc-paper-v1.3.4` tag;
- restricted HGCAL data are described as unavailable, not uploaded.

## Final Checks Before Submit

1. Check the generated Editorial Manager PDF page by page against
   `Paper.pdf`; figure placement, references, and author information must be
   intact.
2. Confirm mandatory uploaded files have the correct portal designation.
3. Resolve every red required-field marker rather than adding filler text.
4. Read the final declaration and submission confirmation screens. Submit
   only after the corresponding author confirms their truthfulness.

## Files In This Kit

- `METADATA.md`: source of record for core portal text.
- `AUTHOR_DECLARATIONS.md`: declarations that require author confirmation.
- `COVER_LETTER.md`: cover-letter draft with remaining author placeholders.
- `UPLOAD_MANIFEST.md`: source archive checksum and artifact links.
- `SUBMISSION_CHECKLIST.md`: final pre-submission checklist.
