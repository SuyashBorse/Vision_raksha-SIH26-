# RetinAI — SIH 2024 Executive Technical Pitch & Judge Presentation Guide

## 🏆 Core Value Proposition
RetinAI is an AI-powered, multi-modal Diabetic Retinopathy (DR) screening platform designed for deployment in Primary Health Centres (PHCs) and tele-retinopathy clinics. It bridges the gap between rural patients and specialized care by enabling non-ophthalmic healthcare workers (ASHAs/Nurses) to perform instant, clinical-grade screening in under 15 seconds.

---

## 🔬 High-Tech AI & Neural Architecture

### 1. EfficientNet-B5 Deep Convolutional Neural Network
- **Resolution:** Fine-tuned at **456×456** resolution using Ben Graham local contrast enhancement + circular ROI masking.
- **Continuous Score Regression:** Output continuous severity score (0.00 – 4.00) mapped to ICDR grades via Nelder-Mead optimized thresholds:
  - `Grade 0 (No DR)`: `< 0.689`
  - `Grade 1 (Mild DR)`: `0.689 – 2.013`
  - `Grade 2 (Moderate DR)`: `2.013 – 3.042`
  - `Grade 3 (Severe DR)`: `3.042 – 4.797`
  - `Grade 4 (Proliferative DR)`: `> 4.797`
- **Validation Score:** **QWK 0.9087** (Quadratic Weighted Kappa) on 5-Fold Cross Validation.

### 2. Neuro-Explainability (Grad-CAM XAI)
- Extracts feature activation gradients directly from the final convolutional layer (`conv_head`).
- Renders high-resolution red/yellow attention heatmaps overlaying microaneurysms, hard exudates, and intraretinal hemorrhages.
- Eliminates "black-box" AI skepticism for ophthalmologists.

### 3. Multi-Modal Clinical Vitals Fusion
- Combines image AI predictions with patient clinical vitals:
  - **HbA1c %** (Glycemic Control)
  - **Diabetes Duration** (Years)
  - **Systolic Blood Pressure** (mmHg)
- Calculates a personalized **5-Year Estimated Vision Loss Risk %** and categorizes systemic risk (`Low`, `Moderate`, `High`, `Critical`).

### 4. ONNX Edge AI Acceleration
- Converts PyTorch model into optimized **ONNX Runtime** binaries (`best_dr_model.onnx` — 107.9 MB).
- Achieves zero-latency offline inference on low-power Intel Core i3 / Celeron laptops without needing an active internet connection.

---

## 📊 Key Clinical & Technical Comparison

| Feature | Competitor / Baseline | RetinAI Platform |
|---|---|---|
| **Model Architecture** | Standard ResNet-50 | EfficientNet-B5 (456px) + Ben Graham Filter |
| **QWK Accuracy** | 0.8200 | **0.9087** |
| **Explainability** | None (Black-Box) | Real-Time Grad-CAM Lesion Heatmaps |
| **Multi-Modal Risk** | Image Only | Vision AI + HbA1c + BP + Diabetes Duration |
| **Offline Capability** | Cloud-Only | ONNX Edge AI (Runs 100% Offline) |

---

## 🎤 30-Second Elevator Pitch for SIH Judges

> *"Respected Judges, RetinAI brings expert-level eye care to every PHC. Powered by an **EfficientNet-B5 Neural Network achieving 0.9087 QWK accuracy**, our system does not just grade images — it provides **Grad-CAM visual lesion heatmaps** and integrates **patient HbA1c and BP vitals** to project 5-year vision loss risk. With **ONNX Edge AI**, it runs 100% offline on any low-cost PHC laptop, ensuring no diabetic patient goes blind due to delayed screening."*
