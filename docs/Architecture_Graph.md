# Architecture_Graph.md
## RetinAI — Dependency Graph
**Legend:** ✅ Done | 🔄 In Progress | ⬜ Pending | ❌ Blocked

---

```
RetinAI
│
├── 📁 docs/                          ✅ DONE
│   ├── PRD_SIH26038.md
│   ├── TRD_SIH26038.md
│   ├── Project_State.md
│   ├── Task_Log.md
│   ├── Current_Sprint.md
│   └── Architecture_Graph.md
│
├── 📁 backend/                        ⬜ PENDING
│   │
│   ├── main.py                        ⬜ BE-001
│   ├── requirements.txt               ⬜ SETUP-002
│   ├── .env.example                   ⬜ SETUP-003
│   ├── Dockerfile                     ⬜ DEP-001
│   │
│   ├── 📁 ai/                         ⬜ PENDING
│   │   ├── quality_checker.py         ⬜ AI-001  (depends: opencv, PIL)
│   │   ├── dr_grader.py               ⬜ AI-002  (depends: timm, torch)
│   │   ├── gradcam.py                 ⬜ AI-003  (depends: AI-002, torchcam)
│   │   ├── findings.py                ⬜ AI-004  (depends: nothing)
│   │   └── pipeline.py                ⬜ AI-005  (depends: AI-001,002,003,004)
│   │
│   ├── 📁 db/                         ⬜ PENDING
│   │   ├── database.py                ⬜ BE-003  (depends: SQLAlchemy)
│   │   └── models.py                  ⬜ BE-002  (depends: BE-003)
│   │
│   ├── 📁 routes/                     ⬜ PENDING
│   │   ├── analyse.py                 ⬜ BE-004  (depends: AI-005, BE-002)
│   │   ├── validate.py                ⬜ BE-005  (depends: BE-002)
│   │   ├── stats.py                   ⬜ BE-006  (depends: BE-002)
│   │   ├── patients.py                ⬜ BE-007  (depends: BE-002)
│   │   ├── report.py                  ⬜ BE-008  (depends: BE-002, ReportLab)
│   │   └── demo.py                    ⬜ BE-009  (depends: AI-005)
│   │
│   ├── 📁 auth/                       ⬜ PENDING
│   │   └── jwt.py                     ⬜ BE-010  (depends: python-jose)
│   │
│   └── 📁 demo_cases/                 ⬜ PENDING
│       ├── grade0_patient.jpg
│       ├── grade2_patient.jpg
│       └── grade4_patient.jpg
│
├── 📁 frontend/                       ⬜ PENDING
│   │
│   ├── public/
│   │   ├── manifest.json              ⬜ PWA-001
│   │   └── sw.js                      ⬜ PWA-002
│   │
│   └── src/
│       ├── App.jsx                    ⬜ FE-001
│       ├── 📁 pages/
│       │   ├── ScreenPage.jsx         ⬜ FE-002 (depends: FE-001)
│       │   ├── ResultPage.jsx         ⬜ FE-003 (depends: FE-002)
│       │   ├── PatientsPage.jsx       ⬜ FE-005 (depends: FE-001)
│       │   ├── DashboardPage.jsx      ⬜ FE-006 (depends: FE-001)
│       │   └── LiveDemoPage.jsx       ⬜ FE-007 (depends: FE-001)
│       │
│       ├── 📁 components/
│       │   ├── ImageCapture.jsx       ⬜ FE-002
│       │   ├── ResultSection.jsx      ⬜ FE-003 (depends: FE-002)
│       │   ├── ValidationButtons.jsx  ⬜ FE-004 (depends: FE-003)
│       │   ├── GradeBadge.jsx         ⬜ FE-003
│       │   ├── HeatmapCompare.jsx     ⬜ FE-003
│       │   ├── StatsCards.jsx         ⬜ FE-006
│       │   └── OfflineBanner.jsx      ⬜ PWA-003
│       │
│       └── 📁 utils/
│           ├── api.js                 ⬜ FE-001 (axios instance)
│           ├── offlineQueue.js        ⬜ PWA-003 (IndexedDB)
│           └── syncManager.js         ⬜ PWA-004
│
├── 📁 notebooks/                      ⬜ PENDING
│   └── train_dr_model.ipynb           ⬜ AI-006  (run on Kaggle)
│
├── 📁 datasets/                       ⬜ PENDING
│   ├── aptos2019/                     ⬜ (download from Kaggle)
│   └── idrid/                         ⬜ (download from IEEE)
│
└── 📁 models/                         ⬜ PENDING
    └── best_dr_model.pth              ⬜ (output of AI-006 training)
```

---

## Dependency Order (Build Sequence)

```
1. SETUP-001 → SETUP-002 → SETUP-003 → SETUP-004
2. AI-001 → AI-002 → AI-003 → AI-004 → AI-005
3. AI-006 (parallel — run on Kaggle)
4. BE-003 → BE-002 → BE-001
5. BE-004 (depends: AI-005 + BE-002)
6. BE-005, BE-006, BE-007, BE-008, BE-009 (parallel after BE-002)
7. BE-010 (auth — can be added last)
8. FE-001 → FE-002 → FE-003 → FE-004 → FE-005 → FE-006 → FE-007
9. PWA-001 → PWA-002 → PWA-003 → PWA-004
10. TEST-001 → TEST-002
11. DEP-001 → DEP-002 → DEP-003
```

---

## Critical Path

```
SETUP-001 → SETUP-002 → BE-003 → BE-002 → AI-002 → AI-003 → AI-005 → BE-004 → FE-003 → DEMO
```
*If any task on the critical path is delayed, the entire demo is delayed.*
