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
