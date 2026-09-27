# 00_scope — Systematic Literature Review Protocol & Scope Specification

This directory houses the normative **PRISMA-P review protocol** and **cryptographic freeze record** for the systematic literature review:  
**"GPS-Denied Navigation for UAVs: A Systematic Literature Review of Multi-Sensor Fusion Approaches (2010–2026)"**.

---

## 1. Directory Structure

```text
00_scope/
├── README.md                      # Directory manifest and protocol summary (this file)
├── FROZEN.md                      # Cryptographic freeze record and hash verification
└── SCOPE.md                       # Normative PRISMA-P protocol and scope document (V2.0)
```

---

## 2. Document Catalog

| Document | Format | Size | SHA256 Hash | Status / Description |
| :--- | :--- | :---: | :--- | :--- |
| [`00_scope/SCOPE.md`](file:///e:/GPS_Denied_SLR/00_scope/SCOPE.md) | Markdown | 13.4 KB | `94E9E287D7BDA1D63224EF48B9C95D633CAB0828EAF2B9164CB092F0499664A4` | **FROZEN PROTOCOL (V2.0)**: Definitive protocol governing research questions Q1–Q8, PICOS criteria, search strategies, and screening inclusion/exclusion boundaries. |
| [`00_scope/FROZEN.md`](file:///e:/GPS_Denied_SLR/00_scope/FROZEN.md) | Markdown | 573 B | `DEE89EB38B21F7B4DA9E2A89C82A2E6349C5CF037CAFD40B13EC9093BF8994BA` | **FREEZE RECORD**: Cryptographic verification anchor certifying Protocol V2.0 re-freeze on 2026-09-27. |

---

## 3. Governance Rule

Per repository governance rules:
* `00_scope/SCOPE.md` is **cryptographically frozen**.
* Any proposal to edit or amend the protocol requires pre-edit backup, formal audit justification, and re-freezing with an updated SHA256 in `FROZEN.md`.
