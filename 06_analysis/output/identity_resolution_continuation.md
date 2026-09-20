# Identity and recovery continuation — 2026-09-17

This note supersedes the conflicting counts and REC_0274 match claim in the conversation. It is not a completed identity audit or evidence extraction.

## Verified state
- Audit v2: 116 DOI_MATCH + 49 SURNAME_MATCH = 165 automated passes.
- REC_0035 is a false-positive SURNAME_MATCH (zhang) and remains quarantined.
- The current proceed_ids.txt has 164 lines, not 165. It has not been expanded in this continuation.
- Active evidence table had zero rows at resumption; no evidence rows were added here.

## Flagged records
| ID | Current disposition | Evidence / limitation |
| --- | --- | --- |
| REC_0023 | Wrong PDF; hold | Master INSPIRE 2025; PDF Khattak et al., arXiv:1903.01656. |
| REC_0035 | Wrong PDF; quarantined | Master Shen WCSP 2020; PDF Bi et al., Robust Autonomous Flight and Mission Management. |
| REC_0053 | Wrong PDF; hold | Master Vision-based Navigation of Unmanned Aerial Vehicles; PDF Maaroof and Bouhlel survey. |
| REC_0115 | Title recovered and matched; metadata discrepancy | Saved workbook title matches master after whitespace normalization. Printed DOI 10.1109/PDCAT.2019.00080 differs from master 10.1109/PDCAT46702.2019.00080. Do not claim DOI_MATCH. |
| REC_0274 | Unresolved; hold | Earlier title-match claim is not substantiated by the available first-page dump. Master ICARCV 2014 DOI 10.1109/ICARCV.2014.7064483; PDF dump contains DOI prefix 10.12716/1001.19. Requires visual title/authors check. |
| REC_1217 | Wrong PDF; hold | Master Vision based UAS navigation for RFI localization; PDF Bayer and Faigl, Localization Fusion for Aerial Vehicles in Partially GNSS Denied Environments. |
| REC_1667 | Wrong PDF; hold | Master Autonomous Mapping and Navigation Unit for Aerial Robots; PDF Nieuwenhuisen et al., Autonomous Navigation for Micro Aerial Vehicles in Complex GNSS-denied Environments. |

## Implemented recovery
The workbook builder now conservatively applies +29 to encoded ASCII glyphs only within REC_0115 spans containing U+0003 (encoded space), preserving literal spaces. Other PDFs and unmarked spans remain unchanged. This is not a letter rotation or a global byte shift. Readable title and abstract are recovered, but unmarked headings, symbols and equations may remain damaged. Visual review is required before numeric extraction.

The builder now accepts --ids for targeted regeneration. The batch digest reads the regenerated workbook, so it needs no duplicate decoder. The older resolver's letter-only caesar_decrypt is still incorrect and its decoded scratch output must not be treated as authoritative.

## Next
1. Verify REC_0274 visually against master title/authors/year; record full PDF DOI.
2. Verify REC_0115 authors and DOI variant, then explicitly decide its proceed-set inclusion. Review figures/equations visually; do not infer NOT_REPORTED from missing regex hits.
3. Keep the five wrong-PDF records out pending corrected PDFs or approved remapping. Do not use the earlier 167 count.
4. Start extraction from the existing 164-ID set with per-paper identity checks, full-page citations, inbox JSON validation and commit gates. Do not rely on digest excerpts alone for absence claims.
5. Replace the quarantine test's zero-row assertion with explicit REC_0035 exclusion when genuine rows are added, preserving its provenance and master-hash checks.
