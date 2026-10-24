# Validation record — October 24, 2026

## Source preservation

Compared the revised `Paper.tex` with baseline commit
`9cc296df1bb4e97b97c5ddf4c025fe47b0936fb7`. The following comparisons passed:

- Numeric-claim macro definitions are unchanged.
- Author registrations, ordering, correspondence marker, affiliations, and
  emails are unchanged.
- All figure blocks, captions, tables, algorithm code, and the usage listing
  are unchanged.
- The exactness proof, recall protocol, table values, FP32 PCA validation
  account, and availability statement are unchanged.
- All 20 `paragraph*` headings and four inline italic complexity labels were
  removed. Normal numbered section and subsection headings remain.
- No figure asset or historical Array/arXiv archive changed.
- `git diff --check` passed.

The source comparison verifies preservation of the validated record. It is
not a new experimental validation of the measurements or FP32 algorithm.

## Manuscript build and appearance

Built with pdfLaTeX/BibTeX through `latexmk`, with shell escape disabled.
The current PDF is 21 A4 pages. The final log contains no unresolved
citations/references or overfull boxes. Three bibliography underfull-box
diagnostics remain; these concern line spacing, not missing content.
`pdffonts` reports all fonts embedded.

Rendered all 21 pages to PNG and inspected a full-document contact sheet.
Inspected the title/abstract, opening physics narrative, reconstruction
connection, and availability/conclusion pages individually. No clipping,
overlap, blank pages, missing figures, or broken glyphs was observed. The
long algorithm occupies a dedicated float page; figure discussions and
their floats remain adjacent. Existing preprint typography is retained.

## Bundle checks

The source ZIP contains 11 files: the main TeX file, compiled BibTeX
bibliography, bibliography source, and eight referenced vector figures.
`unzip -t` passed. The archive was extracted into a fresh directory and
rebuilt successfully to the same 21-page document with resolved references
and no overfull boxes. The separate submission PDF is byte-identical to
root `Paper.pdf`, and `sha256sum -c SHA256SUMS` passed for both deliverables.

No GPU jobs, benchmarks, model training, or new numerical validation were
run. No material was submitted to a journal or messaged to other people.
