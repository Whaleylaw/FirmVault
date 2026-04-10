# File Layout — Medical Records Comprehensive Analysis

Expected layout within the case folder:

```
cases/<slug>/
├── <slug>.md                         # canonical case file (DATA_CONTRACT §2)
├── documents/
│   ├── <complaint>.pdf               # Phase 1 input
│   ├── <police-report>.pdf           # Phase 1 input
│   ├── <depositions>/                # Phase 1 input
│   ├── <discovery>/                  # Phase 1 input
│   ├── <medical-records>.pdf         # Phase 2 input
│   ├── <medical-bills>.pdf           # Phase 2 input
│   ├── _extractions/                 # from document-processing, optional
│   │   └── *.txt, *.tables.json
│   └── analysis/                     # created in Phase 0
│       ├── case_facts.md             # Phase 1
│       ├── inventory.md              # Phase 2a
│       ├── extractions/              # Phase 2b
│       │   ├── <source1>.md
│       │   └── <source2>.md
│       ├── chronology.md             # Phase 2c
│       ├── visits_summary.md         # Phase 2c
│       ├── inconsistencies.md        # Phase 3a
│       ├── red_flags.md              # Phase 3b
│       ├── causation.md              # Phase 3c
│       ├── missing_records.md        # Phase 3d
│       └── FINAL_SUMMARY.md          # Phase 4 — primary deliverable
```

All paths are vault-relative per `DATA_CONTRACT.md` — no `${ROSCOE_ROOT}`, no workspace-relative tricks. When an extraction already exists under `documents/_extractions/`, reuse it instead of re-running the tiered OCR pipeline; the Phase 2b extractors should be able to read either the source PDF or the existing extraction text.
