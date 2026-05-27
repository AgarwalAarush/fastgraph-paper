# LaTeX Formatting Notes

## Float Placement

Large blank areas usually come from over-constraining figures and tables. In
this draft, avoid using `[H]` by default: it forces exact placement, so if the
figure cannot fit at that point LaTeX often leaves a large gap.

Preferred default:

```latex
\begin{figure}[!htbp]
```

Use `[H]` only for small objects that truly must stay exactly at that source
location.

## Preamble Settings

If the paper starts producing blank float pages or large gaps, use permissive
float parameters rather than manually nudging every figure:

```latex
\renewcommand{\topfraction}{0.9}
\renewcommand{\bottomfraction}{0.8}
\renewcommand{\textfraction}{0.07}
\renewcommand{\floatpagefraction}{0.8}

\setcounter{topnumber}{3}
\setcounter{bottomnumber}{2}
\setcounter{totalnumber}{5}
```

These settings give LaTeX more legal placements for floats while still keeping
some text on normal pages.

## Barriers

Use `\FloatBarrier` sparingly. Barriers are useful at major section boundaries,
but if used inside subsections they can force LaTeX to flush pending figures
too early and create blank space.

## Figure Size

Keep large figures below roughly `0.85\textheight`, including captions. If a
figure plus caption is taller than the remaining page area, LaTeX cannot place
it cleanly no matter what float options are used.

For related plots, prefer composite panels over several full-width figures in a
row. This keeps the narrative tight and gives the float algorithm fewer objects
to juggle.

## Practical Policy For This Paper

1. Use `[!htbp]` for most figures and tables.
2. Keep `[H]` only where exact placement is genuinely necessary.
3. Add permissive float parameters in the preamble before doing page-by-page
   manual spacing adjustments.
4. Combine related plots when they naturally read as one result.
5. Rebuild and inspect pages only after applying the global float policy.
