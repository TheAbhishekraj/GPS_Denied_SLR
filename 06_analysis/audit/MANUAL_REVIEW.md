# MANUAL REVIEW — V1 extraction audit

One row required manual inspection during the V1 audit (Phase 2/3).

## REC_1137
- **Flag**: FAIL_TEXT_OCR, short-token ratio 52.5% (threshold 50.0%)
- **Text stats**: 26,871 chars, token count normal, non-ASCII within bounds
- **Diagnosis**: Equation-dense manuscript; LaTeX-rendered subscripts and
  symbols inflate the short-token ratio without any OCR degradation.
- **Disposition**: PASS_EXCEPTION. No re-extraction required.
- **Manuscript note**: Report as "1/171 extraction artefacts required
  manual review; no genuine extraction failures in V1."
