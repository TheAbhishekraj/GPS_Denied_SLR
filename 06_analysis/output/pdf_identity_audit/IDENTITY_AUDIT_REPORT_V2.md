# IDENTITY_AUDIT_REPORT_V2.md

Identity audit on DOI + author surname, not title tokens.

- rows checked: 171
- **DOI_MATCH** (definitive): 116
- **SURNAME_MATCH** (strong): 49
- TITLE_ONLY (inconclusive, needs eyes): 5
- NO_EVIDENCE (presumed wrong PDF): 1
- NO_PDF: 0
- **identity-confirmed (DOI or surname): 165 / 171**
- rows with no testable author surname: 3

A DOI match is definitive. A surname match is strong but not absolute
(a wrong-but-related paper can share an author). TITLE_ONLY means the
title tokens are present but neither the DOI nor any author surname was,
which cannot distinguish identity and must be resolved by hand.

## Why v1 was wrong

v1 reported 170 PASS / 0 FAIL and passed REC_0023, whose PDF is
Khattak et al. (arXiv:1903.01656) while the master row is Variar et al.
(INSPIRE 2025, DOI 10.1109/INSPIRE67328.2025.11300665). The master title
shares 5 of 5 tokens with the Khattak paper's front matter, so a
token-overlap test cannot separate the two. v1 verdicts are superseded.

## Not identity-confirmed

`detected_headline` is the PDF's own opening line, so the file can be
identified without opening it.

| id | verdict | doi? | surnames | title ratio | master title | detected headline |
|---|---|---|---|---|---|---|
| REC_0023 | TITLE_ONLY | False | 0/3 | 1.0 | Autonomous Aerial Navigation in GPS-Denied Environme | Visual–Thermal Landmarks and Inertial Fusion for |
| REC_0053 | TITLE_ONLY | False | 0/3 | 1.0 | Vision-based Navigation of Unmanned Aerial Vehicles | A Survey of Deep Learning Techniques and |
| REC_0115 | NO_EVIDENCE | False | 0/3 | 0.429 | Low Computational Data Fusion Approach Using INS and | /RZ&RPSXWDWLRQDO'DWD)XVLRQ$SSURDFK8VLQJ |
| REC_0274 | TITLE_ONLY | False | 0/1 | 0.857 | Navigation and control of unmanned aerial vehicles i | 1 INTRODUCTION |
| REC_1217 | TITLE_ONLY | False | 0/3 | 1.0 | Vision based UAS navigation for RFI localization | Localization Fusion for Aerial Vehicles in |
| REC_1667 | TITLE_ONLY | False | 0/9 | 1.0 | Autonomous Mapping and Navigation Unit for Aerial Ro | Journal of Intelligent and Robotic Systems manuscrip |
