# BUILD.md — Compilation Instructions for IEEEtran SLR Manuscript
# GPS_Denied_SLR | Author: Abhishek Raj

This document specifies the exact, reproducible build instructions for compiling `GPS_Denied_SLR_IEEE.tex` into a publication-ready PDF using `pdflatex` and `bibtex`.

---

## 1. Prerequisites

Ensure a modern TeX distribution is installed:
- **Windows**: MiKTeX or TeX Live
- **Linux**: TeX Live (`texlive-publishers`, `texlive-science`, `texlive-fonts-recommended`)
- **macOS**: MacTeX

Required packages included in standard TeX distributions:
- `IEEEtran.cls`
- `amsmath`, `amssymb`, `amsfonts`
- `graphicx`, `booktabs`, `multirow`, `cite`, `url`, `hyperref`

---

## 2. Compilation Sequence (2-Pass Build)

From the `07_manuscript/` directory or project root:

```bash
cd E:\GPS_Denied_SLR\07_manuscript

# Pass 1: Generate initial .aux file and citations
pdflatex -interaction=nonstopmode GPS_Denied_SLR_Manuscript_V1_171_COMPLETE.tex

# Pass 2: Process BibTeX bibliography
bibtex GPS_Denied_SLR_Manuscript_V1_171_COMPLETE

# Pass 3: Resolve cross-references and citation labels
pdflatex -interaction=nonstopmode GPS_Denied_SLR_Manuscript_V1_171_COMPLETE.tex

# Pass 4: Finalize layout, hyperlinks, and cross-references
pdflatex -interaction=nonstopmode GPS_Denied_SLR_Manuscript_V1_171_COMPLETE.tex
```

---

## 3. Post-Build Log Verification

Run the following commands in terminal to audit for warnings and errors:

```bash
# Check for undefined citations (must be 0)
grep -i "undefined.*citation" GPS_Denied_SLR_Manuscript_V1_171_COMPLETE.log

# Check for undefined references (must be 0)
grep -i "undefined.*reference" GPS_Denied_SLR_Manuscript_V1_171_COMPLETE.log

# Check for overfull horizontal boxes (must be < 5)
grep -c "Overfull \\hbox" GPS_Denied_SLR_Manuscript_V1_171_COMPLETE.log
```

---

## 4. Figures and Asset Paths

All 9 figures are located in:
`../06_analysis/output/figures_v2/`

- `fig01_publication_trends.png`
- `fig02_platform_distribution.png`
- `fig03_environment_distribution.png`
- `fig04_method_evolution.png`
- `fig05_sensor_frequency.png`
- `fig06_application_domains.png`
- `fig07_prisma_flow.png`
- `fig08_method_environment_heatmap.png`
- `fig09_research_maturity_radar.png`
