# 👁️ RetinAI — Explainable AI for Automated Diabetic Retinopathy Screening
## Problem Statement: SIH26038 · MathWorks · Smart India Hackathon 2026

[![SIH 2026](https://img.shields.io/badge/SIH-2026-orange.svg)](https://www.sih.gov.in/)
[![Problem Statement](https://img.shields.io/badge/Problem%20Statement-SIH26038-blue.svg)](../../README.md)
[![Organisation](https://img.shields.io/badge/Organisation-MathWorks-red.svg)](https://www.mathworks.com/)
[![Sensitivity](https://img.shields.io/badge/Sensitivity%20(L2%2B)-96.0%25-brightgreen.svg)](../../README.md#-clinical-benchmark--validation-results)
[![Specificity](https://img.shields.io/badge/Specificity%20(L2%2B)-97.0%25-brightgreen.svg)](../../README.md#-clinical-benchmark--validation-results)
[![Tests](https://img.shields.io/badge/Tests-82%2F82%20Passing%20(100%25)-success.svg)](../../README.md#-test-suite--verification)

> For the comprehensive master documentation, architecture diagrams, and clinical benchmark tables, see the root **[`../../README.md`](../../README.md)**.

---

## ⚡ Quick Start

### 1. MATLAB Clinical Pipeline & Simulink Simulation
Open MATLAB and execute the master orchestrator:
```matlab
cd matlab
dr_pipeline_demo
```
* Or run the Simulink district screening model independently:
```matlab
cd matlab/simulink
results = run_simulation();
plot_results(results);
```

### 2. Python Clinical Benchmark & Ablation Study
Validate sensitivity (>90%) and specificity (>85%) on referable DR:
```powershell
backend\venv\Scripts\python.exe notebooks\validate_benchmarks.py
```

### 3. Running the Full Production Platform (Backend + React PWA)
Use the automated startup script:
```powershell
.\scripts\start_dev.ps1
```
* Or start components manually in two terminals:*
* **Terminal 1 — Backend (FastAPI):**
  ```powershell
  cd backend
  .\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
  ```
* **Terminal 2 — Frontend (React 19 Dashboard):**
  ```powershell
  cd frontend\dr-dashboard
  npm run dev
  ```
Open **`http://localhost:5173`** in your browser.

---

## 🔬 Directory Overview

```
dr-screening/
├── matlab/                           ← MATLAB & SIMULINK CLINICAL PIPELINE
│   ├── dr_pipeline_demo.m            ← Master orchestrator running all 5 modules
│   ├── quality_assessment.m          ← Quality gate (Laplacian, FOV, Hue) + CLAHE
│   ├── segment_retina.m              ← OD, fovea, Frangi vessels, MA, exudates, hem, NV
│   ├── grade_dr.m                    ← DR grader (ONNX/PTH import + TTA)
│   ├── explain_gradcam.m             ← Grad-CAM heatmap + lesion evidence table
│   ├── compute_metrics.m             ← Sensitivity, specificity, QWK, ROC curves
│   └── simulink/
│       ├── build_screening_model.m   ← Programmatically builds .slx model & runs simulation
│       ├── run_simulation.m          ← 4 operational scenarios (Baseline, Rural, Opt, Scale)
│       └── plot_results.m            ← Wait times, heatmap, annual capacity
│
├── backend/                          ← FASTAPI ASYNC BACKEND (PORT 8000)
│   ├── main.py                       ← Application lifespan & routing
│   ├── ai/                           ← Quality gate, DR grader, Grad-CAM, segmentation
│   ├── routes/                       ← Screening, validation, FHIR report, demo endpoints
│   ├── db/                           ← SQLAlchemy SQLite/PostgreSQL models
│   └── tests/                        ← 82/82 passing automated unit & integration tests
│
├── frontend/dr-dashboard/            ← REACT 19 + VITE + TAILWIND PWA (PORT 5173)
│   ├── src/                          ← Image capture, Grad-CAM viewer, voice readout
│   └── public/sw.js                  ← 100% offline IndexedDB background sync
│
├── models/                           ← TRAINED DL WEIGHTS
│   ├── best_dr_model.pth             ← PyTorch EfficientNet-B5 weights (~109 MB)
│   └── best_dr_model.onnx            ← Quantized ONNX Edge weights (~108 MB)
│
└── notebooks/
    └── validate_benchmarks.py        ← Statistical validation & ablation study runner
```

---

## 📊 Summary of Validated Performance
* **Referable DR Sensitivity (L2+)**: **`96.00%`** (Target: $>90.0\%$)
* **Referable DR Specificity (L2+)**: **`97.00%`** (Target: $>85.0\%$)
* **Quadratic Weighted Kappa (QWK)**: **`0.9669`**
* **Backend Test Suite**: **`82 / 82 passed (100%)`**
