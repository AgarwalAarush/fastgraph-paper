# arXiv Source Bundle

`FastGraph-arXiv-source.zip` contains `Paper.tex`, `Paper.bbl`,
`references.bib`, and the eight referenced vector figures under `media/`.
It excludes the compiled manuscript PDF, auxiliary build files, unused
figures, and journal submission materials.

Select `Paper.tex`, pdfLaTeX, and TeX Live 2023 during upload. A fresh
extraction compiles with shell escape disabled and the included `.bbl`.
The current preprint is 20 pages, with 11-point Computer Modern text,
a narrower text block, and individual author/affiliation/email entries.
The author order and corresponding author are preserved.

`Paper.pdf` in the repository root is the matching preview. Earlier
journal-specific files under `submission/array/` remain historical copies.
This bundle supersedes the earlier ZIP generated in the workspace temp
directory. Inspect the PDF produced by arXiv before completing submission.

After future manuscript edits, rebuild and regenerate this archive; the ZIP
is a snapshot and does not update automatically.

## Checked Float Locations

| Material | PDF page(s) |
|---|---|
| Algorithm 1, directly below the pseudocode explanation | 6 |
| Listing 1, kept together before Experimental Setup | 8 |
| Figure 1, headline plot and speedup table | 9 |
| Figures 2 and 3, dataset-size and neighborhood-size scaling | 10 |
| Figure 4 and Table 1, synthetic results | 11 |
| Figure 5, memory footprint | 12 |
| Table 2 and Figure 6, binning ablation and CLOVER results | 13 |
| Table 3 and Figure 7, recall evaluation | 14–15 |

All figures and tables appear on the same page as their discussion or the
next page. The recall figure is kept before the subsequent integration
subsection. Page locations must be checked again after future edits.
