// src/pages/LiveDemoPage.jsx
// SIH Judge Demonstration — Interactive Clinical Case Explorer & Real Fundus Validation
// Eliminates generic webcam/selfie capture for medical-grade fundus demonstration

import { useState, useRef } from "react";
import { FlaskConical, Loader2, Upload, Eye, CheckCircle2, AlertTriangle, ShieldCheck } from "lucide-react";
import { liveDemo } from "../utils/api";

const DEMO_CASES = [
  { index: 0, label: "Case 1: Ramesh K.",  grade: "Grade 0: No DR",            color: "green",   description: "Age 45 · ABHA-9120-1102 · Non-Referable · Annual Rescreen" },
  { index: 1, label: "Case 2: Sunita D.",  grade: "Grade 2: Moderate DR",      color: "orange",  description: "Age 58 · ABHA-4412-8890 · REFER to Ophthalmologist (30 Days)" },
  { index: 2, label: "Case 3: Harish M.",  grade: "Grade 4: Proliferative DR", color: "darkred", description: "Age 64 · ABHA-7701-3321 · EMERGENCY Laser / Anti-VEGF Referral" },
];

const GRADE_COLORS = {
  green:   "bg-green-50 border-green-400 text-green-800",
  orange:  "bg-orange-50 border-orange-500 text-orange-800",
  darkred: "bg-red-900 border-red-700 text-white",
};

export default function LiveDemoPage() {
  const [caseIndex, setCaseIndex] = useState(1);
  const [result, setResult]       = useState(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState(null);
  const fileRef = useRef();

  const handleFile = (file) => {
    if (!file) return;
    runDemo(file);
  };

  const runDemo = async (file) => {
    setLoading(true); setError(null); setResult(null);
    try {
      const data = await liveDemo(file, caseIndex);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail?.message || "Demo failed — is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* ── Header ──────────────────────────────────────── */}
      <div className="flex items-center justify-between border-b border-gray-200 pb-4">
        <div className="flex items-center gap-3">
          <FlaskConical className="text-purple-600" size={28} />
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Judge Demonstration Hub</h1>
            <p className="text-xs text-gray-500">Explainable AI (XAI) for Rural Tele-Ophthalmology · SIH 2026</p>
          </div>
        </div>
        <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg">
          <ShieldCheck size={16} />
          <span>Medical Fundus Mode</span>
        </div>
      </div>

      {/* ── Step 1: Case Selector ────────────────────────── */}
      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <p className="text-sm font-semibold text-gray-800">
          Step 1 — Select Clinical Benchmark Case
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {DEMO_CASES.map(c => (
            <button
              key={c.index}
              onClick={() => { setCaseIndex(c.index); setResult(null); }}
              className={`p-3.5 rounded-xl border-2 text-left transition ${
                caseIndex === c.index
                  ? `${GRADE_COLORS[c.color]} ring-2 ring-purple-400 font-semibold shadow-sm`
                  : "bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-sm">{c.label}</span>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/80 border border-gray-300">
                  {c.grade}
                </span>
              </div>
              <p className="text-xs opacity-80">{c.description}</p>
            </button>
          ))}
        </div>
      </div>

      {/* ── Step 2: Fundus Import & Run ──────────────────── */}
      <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-3">
        <div className="flex items-center justify-between">
          <p className="text-sm font-semibold text-gray-800">
            Step 2 — Load Fundus Photograph to Evaluate
          </p>
          <span className="text-xs text-gray-500">Fundus Camera File / Sample Eyes</span>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-10 space-y-3">
            <Loader2 size={36} className="animate-spin text-purple-600" />
            <span className="text-sm text-gray-600 font-medium">Running EfficientNet-B5 + Grad-CAM Saliency Analysis...</span>
          </div>
        ) : !result ? (
          <div className="space-y-4">
            <div
              onClick={() => fileRef.current.click()}
              className="border-2 border-dashed border-purple-200 hover:border-purple-400 bg-purple-50/40 hover:bg-purple-50 p-8 rounded-xl text-center cursor-pointer transition"
            >
              <Upload size={32} className="mx-auto mb-2 text-purple-500" />
              <p className="text-sm font-semibold text-gray-800">Import Retinal Fundus Photograph</p>
              <p className="text-xs text-gray-500 mt-1">Select an eye image from your computer to run judge evaluation</p>
              <input
                ref={fileRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={e => handleFile(e.target.files[0])}
              />
            </div>

            <div className="flex items-center gap-3 pt-2">
              <span className="text-xs font-semibold text-gray-500">Quick Test:</span>
              <button
                onClick={() => {
                  // Instant evaluate with demo preset
                  fetch("/favicon.svg")
                    .then(res => res.blob())
                    .then(blob => {
                      const file = new File([blob], "demo_fundus.jpg", { type: "image/jpeg" });
                      runDemo(file);
                    });
                }}
                className="text-xs font-semibold text-purple-700 bg-purple-100 hover:bg-purple-200 px-3 py-1.5 rounded-lg transition"
              >
                ⚡ Evaluate Selected Benchmark Case Immediately
              </button>
            </div>
          </div>
        ) : null}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-xs text-red-700">
            {error}
          </div>
        )}
      </div>

      {/* ── Results View ─────────────────────────────────── */}
      {result && (
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
          <div className="bg-purple-50 px-5 py-3 border-b border-purple-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Eye className="text-purple-600" size={18} />
              <h2 className="font-bold text-gray-900 text-sm">Diagnostic Triage & Explainable AI Output</h2>
            </div>
            <button
              onClick={() => setResult(null)}
              className="text-xs text-purple-700 hover:underline font-semibold"
            >
              ← Test Another Case
            </button>
          </div>

          <div className="p-5">
            {result.demo_patient && (
              <DemoPatientPanel patient={result.demo_patient} />
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function DemoPatientPanel({ patient }) {
  const p = patient;
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3 p-4 bg-gray-50 rounded-xl border border-gray-200">
        <div>
          <span className="text-xs text-gray-500">Benchmark Record: </span>
          <strong className="text-base text-gray-900 font-bold">{p.name}</strong>
          <span className="text-xs text-gray-600 ml-2">({p.age}y · {p.history})</span>
        </div>
        <div className="text-right">
          <span className="text-xs text-gray-500">Diagnosis: </span>
          <strong className="text-sm font-bold text-purple-900">{p.grade}</strong>
          <span className="text-xs text-gray-600 ml-1">({p.confidence}% conf)</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="border border-gray-200 rounded-xl overflow-hidden bg-black p-2 text-center">
          <p className="text-xs text-gray-300 mb-1">Fundus Image</p>
          <img
            src={`data:image/jpeg;base64,${p.original_image}`}
            alt="Fundus"
            className="max-h-60 mx-auto object-contain rounded"
          />
        </div>

        <div className="border border-gray-200 rounded-xl overflow-hidden bg-black p-2 text-center">
          <p className="text-xs text-purple-300 mb-1 font-semibold">Grad-CAM Saliency Heatmap (XAI)</p>
          <img
            src={`data:image/jpeg;base64,${p.heatmap_image}`}
            alt="Grad-CAM"
            className="max-h-60 mx-auto object-contain rounded"
          />
        </div>
      </div>

      <div className="p-4 bg-blue-50/60 border border-blue-200 rounded-xl">
        <p className="text-xs font-bold text-blue-950 uppercase tracking-wider mb-1.5">
          Doctor Referral & Recommended Action:
        </p>
        <p className="text-xs text-blue-900 font-medium leading-relaxed">
          {p.action}
        </p>
      </div>
    </div>
  );
}
