# Proposed new CPC submission — October 24, 2026

The manuscript addresses the September 20 desk-rejection comments on
COMPHY-D-26-01041. It foregrounds calorimeter shower reconstruction, explains
neighbor search for a general computational-physics audience, and replaces
the report-like paragraph headings with connected prose. It preserves the
author order and validated experimental record.

## Review files

- [Revised manuscript PDF](FastGraph-CPC-2026-10-24.pdf)
- [Submission source ZIP](FastGraph-CPC-2026-10-24-source.zip)
- [Change log and preservation audit](CHANGELOG.md)
- [Claims and decisions requiring author confirmation](AUTHOR_CONFIRMATIONS.md)
- [Response to the CPC editor](EDITOR_RESPONSE.md)
- [Cover-letter draft](COVER_LETTER.md)
- [Portal metadata](METADATA.md)
- [Build and packaging checks](VALIDATION.md)

The PDF and ZIP are prepared for coauthor review. Resolve the author flags
before submitting. In particular, the earlier CPC paper was rejected with an
invitation to submit a new paper; the separate Array review process described
in the pasted conversation is not a CPC revision invitation.

## Source bundle

The ZIP contains `Paper.tex`, `Paper.bbl`, `references.bib`, and the eight
referenced PDF figure assets under `media/`. It does not include restricted
CMS data, internal correspondence, author questions, or the historical
submission packages. The separate PDF matches the current root `Paper.pdf`.

Build with pdfLaTeX and BibTeX, or:

```sh
latexmk -pdf -pdflatex='pdflatex -no-shell-escape %O %S' \
  -interaction=nonstopmode -halt-on-error Paper.tex
```

`SHA256SUMS` records the PDF and ZIP hashes. The original
`pca-fgc-paper-v1.3.4` tags still identify the measured experimental
artifacts; the new manuscript is not represented as that historical source.
No material was submitted to a journal or sent to coauthors.
