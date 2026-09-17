# REC_0035 extraction quarantine

Status: INVALID ATTRIBUTION; not an extracted paper or a non-reporting result.

The three original artifacts in this directory are preserved unchanged for audit:
`MASTER_EVIDENCE_V1.csv` (one row), `REC_0035.json`, and `REC_0035.md`.
Do not merge these files back into the active extraction inbox.

## Direct source check

- Expected master identity: **State Estimation and Control for Micro Aerial
  Vehicles in GPS-denied Environments**, H. Shen; X. Zhang; H. Lu; B. Tian;
  Q. Zong (2020), DOI `10.1109/WCSP49889.2020.9299710`.
- Actual local PDF, page 1: **Robust Autonomous Flight and Mission Management
  for MAVs in GPS-denied Environments**, Yingcai Bi, Menglu Lan, Jiaxin Li,
  Kun Zhang, Hailong Qin, Shupeng Lai, Ben M. Chen.
- Actual local PDF, page 5: average translation error of Hector SLAM is
  **0.071 m**, and Cartographer SLAM is **0.059 m**, with VICON ground truth.
  These values belong to the actual Bi et al. PDF, not the master identity.
- The invalid extraction also describes a ground robot and a comparison-only
  contribution; the actual abstract describes an integrated MAV flight system.

Source PDF: `E:\GPS_Denied_SLR\05_papers_fulltext\REC_0035.pdf`.
Neither the PDF nor the audited master has been changed.
The active evidence CSV is restored to its existing 63-column header, with
zero rows. This is an incomplete extraction, not a completed empty corpus.
Do not substitute NOT_REPORTED for unresolved identity or unread evidence.

## Other blocking observations

Direct page-1 inspection also confirms REC_0023's master identity (Variar et al.,
Autonomous Aerial Navigation in GPS-Denied Environments) disagrees with its PDF
(Khattak, Papachristos, Alexis, Visual-Thermal Landmarks and Inertial Fusion for
Navigation in Degraded Visual Environments, arXiv:1903.01656).
The earlier automated identity PASS labels cannot establish publication identity:
matching a surname or a DOI in references is insufficient.

The numeric probe's 44 matching files are candidates, NOT a measured reporting
rate. Neither 127 nonmatching PDFs nor a substantial text layer proves absence
of numeric results in tables or figures. No final reporting-gap finding or V9.1
verdict is justified yet. Inspect every paper after resolving its identity.

## Resume requirements

Obtain the correct PDFs for the existing IDs, or have the corpus owner approve
an explicit identity remapping and its implications for QA. Never silently
replace the audited master or transfer its QA to different publications.
Review title/authors on the first page against master identity before extraction.
The manuscript and human verification sample remain blocked.

Validation: `E:\GPS_Denied_SLR\06_analysis\scripts\test_rec0035_quarantine.py`.
The zero-row assertion is a checkpoint-specific test, to be updated when genuine
identity-verified extractions are added.
