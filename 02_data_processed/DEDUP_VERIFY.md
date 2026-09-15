# DEDUP_VERIFY.md — Deduplication Verification Audit
# Timestamp: 2026-09-15 22:52:26

## Verification Summary

- **Deduplicated Master Records**: 1719 (Target: 1,719) — `PASS`
- **Deduplication Log Entries**: 281 (Target: 281) — `PASS`
- **Duplicate Reasons Present**: ['DOI match', 'Title match']
- **Reasons Limited to 'DOI match' or 'Title match'**: True — `PASS`

## Deduplication Method Recap
1. **DOI Normalization & Exact Match**: Lowercase, strip `https://doi.org/`, exact string match.
2. **Fuzzy Title Matching**: Lowercase, strip punctuation and whitespace, Levenshtein ratio >= 0.90.
3. **Tie-Breaking Rule**: Keep IEEE Xplore record if available; otherwise older year; otherwise lexicographically smaller DOI.
4. **Removal Rate**: 281 duplicates removed from 2,000 raw records (14.05% ≈ 14.1%).

## Conclusion
Deduplication dataset integrity verified. All records trace to source database rows without dropped or undocumented items.
