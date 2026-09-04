# RetinAI — Explainable AI for Diabetic Retinopathy Screening
## SIH26038 · MathWorks · SIH 2026

---

## Quick Start

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend/dr-dashboard
npm install
npm start
```

## Project Structure

```
dr-screening/
├── backend/          ← FastAPI + AI pipeline
│   ├── ai/           ← Quality checker, DR grader, Grad-CAM
│   ├── db/           ← SQLAlchemy models + sessions
│   ├── routes/       ← API endpoints
│   ├── auth/         ← JWT auth
│   └── demo_cases/   ← Pre-loaded demo patient images
├── frontend/         ← React PWA
├── notebooks/        ← Kaggle training notebooks
├── models/           ← Trained .pth model files
├── datasets/         ← APTOS 2019 + IDRiD data
└── docs/             ← PRD, TRD, project memory
```

## Docs
- [PRD](../docs/PRD_SIH26038.md)
- [TRD](../docs/TRD_SIH26038.md)
- [Architecture](../docs/Architecture_Graph.md)
