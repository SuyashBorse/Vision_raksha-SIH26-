# Project_State.md
## RetinAI — Explainable AI for Diabetic Retinopathy Screening
### SIH26038 · MathWorks · SIH 2026

---

## Project Info

| Field | Value |
|-------|-------|
| Project Name | RetinAI |
| PS Number | SIH26038 |
| Version | 0.0.1 (Init) |
| Current Sprint | Sprint 1 — Project Setup & AI Pipeline |
| Sprint Start | 2026-08-29 |
| Deadline | 2026-09-20 |

---

## Module Status

| Module | Status | Owner |
|--------|--------|-------|
| Project Setup (folder structure, env) | ⬜ NOT STARTED | All |
| Dataset Download & Preprocessing | ⬜ NOT STARTED | Member 6 |
| AI — Quality Checker (MobileNetV3) | ⬜ NOT STARTED | Member 2 |
| AI — DR Grader (EfficientNet-B4) | ⬜ NOT STARTED | Member 1 |
| AI — Segmentation (U-Net) | ⬜ NOT STARTED | Member 2 |
| AI — Grad-CAM Engine | ⬜ NOT STARTED | Member 2 |
| AI — Model Training Pipeline | ⬜ NOT STARTED | Member 1 |
| Backend — FastAPI Setup | ⬜ NOT STARTED | Member 3 |
| Backend — /api/analyse endpoint | ⬜ NOT STARTED | Member 3 |
| Backend — /api/validate endpoint | ⬜ NOT STARTED | Member 3 |
| Backend — /api/stats endpoint | ⬜ NOT STARTED | Member 3 |
| Backend — /api/patients endpoint | ⬜ NOT STARTED | Member 3 |
| Backend — /api/report endpoint | ⬜ NOT STARTED | Member 3 |
| Backend — /api/live-demo endpoint | ⬜ NOT STARTED | Member 3 |
| Backend — Database Schema (SQLite) | ⬜ NOT STARTED | Member 3 |
| Backend — PDF Report Generator | ⬜ NOT STARTED | Member 6 |
| Backend — Auth (JWT) | ⬜ NOT STARTED | Member 3 |
| Frontend — React Setup + Routing | ⬜ NOT STARTED | Member 4 |
| Frontend — Upload / Camera Component | ⬜ NOT STARTED | Member 4 |
| Frontend — Result / Heatmap View | ⬜ NOT STARTED | Member 4 |
| Frontend — Doctor Validation UI | ⬜ NOT STARTED | Member 4 |
| Frontend — Patient Records UI | ⬜ NOT STARTED | Member 4 |
| Frontend — Analytics Dashboard | ⬜ NOT STARTED | Member 4 |
| Mobile — PWA Config | ⬜ NOT STARTED | Member 5 |
| Mobile — Offline Queue (IndexedDB) | ⬜ NOT STARTED | Member 5 |
| Mobile — Service Worker (Workbox) | ⬜ NOT STARTED | Member 5 |
| Mobile — Auto-sync on reconnect | ⬜ NOT STARTED | Member 5 |
| Demo — 3 Pre-loaded patient cases | ⬜ NOT STARTED | Member 6 |
| Demo — Live demo endpoint | ⬜ NOT STARTED | Member 3 |
| Testing — Unit tests (backend) | ⬜ NOT STARTED | Member 6 |
| Testing — API integration tests | ⬜ NOT STARTED | Member 6 |
| Deploy — Render.com (backend) | ⬜ NOT STARTED | Member 3 |
| Deploy — Vercel (frontend) | ⬜ NOT STARTED | Member 4 |

---

## Completed Modules
*None yet — project initializing.*

---

## Blockers
*None currently.*

---

## Technical Decisions (from TRD)

| Decision | Choice | Reason |
|----------|--------|--------|
| AI Framework | PyTorch 2.2 + timm | Industry standard, EfficientNet-B4 available |
| DR Model | EfficientNet-B4 | Best accuracy-speed for 380x380 |
| Explainability | Grad-CAM (torchcam) | Fastest, clinical deployment balance |
| Backend | FastAPI + Uvicorn | Async, auto-docs |
| Database (dev) | SQLite | Zero-setup |
| Database (prod) | PostgreSQL (Supabase free) | ACID, free tier |
| Frontend | React 18 + Tailwind CSS | Component model, rapid UI |
| PWA / Offline | Workbox Service Worker | IndexedDB queuing |
| Image Storage | Cloudinary (free 25GB) | CDN + base64 fallback |
| Auth | JWT (HS256) | Stateless |
| PDF | ReportLab | Python-native |
| GPU Training | Kaggle Notebooks (P100) | Free, 30hrs/week |
| Backend Host | Render.com (free) | Docker-compatible |
| Frontend Host | Vercel (free) | Global CDN |

---

## Architecture Decisions

- Monolith FastAPI for V1 (SIH demo) — microservices deferred to V2
- SQLite for prototype, PostgreSQL for production
- CPU inference only for Render.com free tier
- INT8 quantization applied for speed
- Offline-first: IndexedDB + Background Sync API

---

## API Contract (Base)

- Base URL: `http://localhost:8000` (dev) / `https://retinai-backend.onrender.com` (prod)
- Auth: Bearer JWT
- Content-Type: application/json (except file uploads)
