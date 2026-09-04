// src/pages/LiveDemoPage.jsx
// SIH judge demo — eye detection on live photo + pre-loaded patient results
// Spec: TRD /api/live-demo, sih26038_live_demo.md

import { useState, useRef } from "react";
import { Camera, FlaskConical, Loader2 } from "lucide-react";
import { liveDemo } from "../utils/api";

const DEMO_CASES = [
  { index: 0, label: "Patient A",  grade: "No DR",            color: "green",   description: "Age 45 · Diabetic 3 yrs · Annual rescreen" },
  { index: 1, label: "Patient B",  grade: "Moderate DR",      color: "orange",  description: "Age 52 · Diabetic 8 yrs · REFER" },
  { index: 2, label: "Patient C",  grade: "Proliferative DR", color: "darkred", description: "Age 61 · Diabetic 15 yrs · EMERGENCY" },
];

const GRADE_COLORS = {
  green:   "bg-green-50 border-green-400 text-green-800",
  yellow:  "bg-yellow-50 border-yellow-400 text-yellow-800",
  orange:  "bg-orange-50 border-orange-500 text-orange-800",
  red:     "bg-red-50 border-red-500 text-red-800",
  darkred: "bg-red-900 border-red-700 text-white",
};

export default function LiveDemoPage() {
  const [caseIndex, setCaseIndex] = useState(1);        // default: Moderate DR (most impressive)
  const [result, setResult]       = useState(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState(null);

  const fileRef   = useRef();
  const videoRef  = useRef();
  const streamRef = useRef();
  const [cameraOn, setCameraOn] = useState(false);

  // ── Camera ────────────────────────────────────────────
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      streamRef.current   = stream;
      videoRef.current.srcObject = stream;
      setCameraOn(true);
    } catch {
      setError("Camera unavailable — please upload a photo instead.");
    }
  };

  const captureAndAnalyse = () => {
    const canvas = document.createElement("canvas");
    canvas.width  = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext("2d").drawImage(videoRef.current, 0, 0);
    canvas.toBlob((blob) => {
      const file = new File([blob], "judge_photo.jpg", { type: "image/jpeg" });
      streamRef.current?.getTracks().forEach(t => t.stop());
      setCameraOn(false);
      runDemo(file);
    }, "image/jpeg", 0.9);
  };

  const stopCamera = () => {
    streamRef.current?.getTracks().forEach(t => t.stop());
    setCameraOn(false);
  };

  // ── File upload path ──────────────────────────────────
  const handleFile = (file) => {
    if (!file) return;
    runDemo(file);
  };

  // ── Core demo call ────────────────────────────────────
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

  const reset = () => { setResult(null); setError(null); };

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">

      {/* ── Header ──────────────────────────────────────── */}
      <div className="flex items-center gap-3">
        <FlaskConical className="text-purple-600" size={28} />
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Live Demo</h1>
          <p className="text-sm text-gray-500">SIH 2026 Judge Demonstration — Explainable AI DR Screening</p>
        </div>
      </div>

      {/* ── Demo case selector ───────────────────────────── */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <p className="text-sm font-semibold text-gray-700 mb-3">
          Step 1 — Select Pre-loaded Patient Case
        </p>
        <div className="grid grid-cols-3 gap-3">
          {DEMO_CASES.map((c) => (
            <button
              key={c.index}
              onClick={() => { setCaseIndex(c.index); reset(); }}
              className={`rounded-xl border-2 p-3 text-left transition
                ${caseIndex === c.index
                  ? "border-purple-500 bg-purple-50"
                  : "border-gray-200 hover:border-purple-300 hover:bg-purple-50/40"}`}
            >
              <p className="font-bold text-sm text-gray-800">{c.label}</p>
              <p className={`text-xs font-semibold mt-1 px-2 py-0.5 rounded-full inline-block
                ${GRADE_COLORS[c.color]}`}>
                {c.grade}
              </p>
              <p className="text-xs text-gray-400 mt-1">{c.description}</p>
            </button>
          ))}
        </div>
      </div>

      {/* ── Photo capture ────────────────────────────────── */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <p className="text-sm font-semibold text-gray-700 mb-3">
          Step 2 — Take Judge's Photo (for eye detection demo)
        </p>

        {cameraOn ? (
          <div className="space-y-3">
            <div className="relative rounded-xl overflow-hidden bg-black aspect-video max-h-64">
              <video ref={videoRef} autoPlay playsInline className="w-full h-full object-cover" />
              <div className="absolute bottom-3 inset-x-0 flex justify-center gap-3">
                <button onClick={captureAndAnalyse}
                  className="bg-white text-purple-700 font-bold px-6 py-2 rounded-full shadow hover:bg-purple-50 transition">
                  📸 Capture & Analyse
                </button>
                <button onClick={stopCamera}
                  className="bg-white/20 text-white px-4 py-2 rounded-full">
                  Cancel
                </button>
              </div>
            </div>
          </div>
        ) : loading ? (
          <div className="flex items-center justify-center py-6">
            <Loader2 size={32} className="animate-spin text-purple-500" />
            <span className="ml-3 text-gray-500 text-sm">Detecting eye + loading patient result...</span>
          </div>
        ) : !result ? (
          <div className="flex gap-3">
            <button onClick={startCamera}
              className="flex-1 flex items-center justify-center gap-2 bg-purple-700 text-white
                         py-3 rounded-xl font-semibold hover:bg-purple-800 transition">
              <Camera size={18} /> Open Camera
            </button>
            <button onClick={() => fileRef.current.click()}
              className="flex-1 flex items-center justify-center gap-2 border-2 border-purple-300
                         text-purple-700 py-3 rounded-xl font-semibold hover:bg-purple-50 transition">
              📁 Upload Photo
            </button>
            <input ref={fileRef} type="file" accept="image/*" className="hidden"
              onChange={e => handleFile(e.target.files[0])} />
          </div>
        ) : null}

        {error && (
          <p className="mt-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
            {error}
          </p>
        )}
      </div>

      {/* ── Results — dual panel ─────────────────────────── */}
      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

          {/* Left — Live photo + eye detection */}
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div className="px-4 py-3 border-b border-gray-100 flex items-center gap-2">
              <div className={`w-2.5 h-2.5 rounded-full ${result.live_photo?.eye_detected ? "bg-green-500" : "bg-gray-400"}`} />
              <p className="text-sm font-semibold text-gray-700">
                Judge's Photo — {result.live_photo?.eye_detected ? "Eye Detected ✓" : "No Eye Detected"}
              </p>
            </div>
            {result.live_photo?.annotated_image && (
              <img
                src={`data:image/jpeg;base64,${result.live_photo.annotated_image}`}
                alt="Judge annotated photo"
                className="w-full object-contain bg-gray-900 max-h-64"
              />
            )}
            <p className="px-4 py-2 text-xs text-gray-400">{result.live_photo?.message}</p>
          </div>

          {/* Right — Demo patient result */}
          {result.demo_patient && (
            <DemoPatientPanel patient={result.demo_patient} />
          )}
        </div>
      )}

      {result && (
        <div className="flex justify-center">
          <button onClick={reset}
            className="text-sm text-gray-400 hover:text-purple-600 transition">
            ↺ Run Demo Again
          </button>
        </div>
      )}

      {/* ── Judge talking points ─────────────────────────── */}
      <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl border border-blue-200 p-5">
        <p className="text-sm font-bold text-blue-800 mb-3">💬 Key Points for Judges</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-blue-700">
          {[
            "🔴 Red zones on heatmap = where AI detected lesions",
            "📊 Every existing product is a black box — ours explains WHY",
            "📱 Works offline in rural areas (PWA + IndexedDB)",
            "💰 < ₹1 per screening vs ₹500–2000 manual cost",
            "🎯 91.3% sensitivity — outperforms average GP",
            "🇮🇳 Fine-tuned on IDRiD — Indian patient dataset",
          ].map((point) => (
            <div key={point} className="flex items-start gap-2 bg-white/60 rounded-lg px-3 py-2">
              <span>{point}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Demo patient result panel ─────────────────────────────────
function DemoPatientPanel({ patient }) {
  const colorClass = GRADE_COLORS[patient.color] ?? GRADE_COLORS.green;

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100">
        <p className="text-sm font-semibold text-gray-700">AI Screening Result</p>
        <p className="text-xs text-gray-400">{patient.name}</p>
      </div>

      {/* Grade banner */}
      <div className={`mx-4 mt-3 rounded-lg border-2 p-3 ${colorClass}`}>
        <div className="flex justify-between items-center">
          <div>
            <p className="font-bold">Grade {patient.grade} — {patient.grade_label}</p>
            <p className="text-xs mt-0.5">{patient.action}</p>
          </div>
          <p className="text-2xl font-bold">{patient.confidence}%</p>
        </div>
      </div>

      {/* Images */}
      <div className="grid grid-cols-2 gap-0 mt-3 border-t border-gray-100">
        <div className="border-r border-gray-100">
          <p className="text-xs text-center text-gray-400 py-1">Fundus Image</p>
          <img src={`data:image/jpeg;base64,${patient.fundus_image}`}
            alt="fundus" className="w-full max-h-32 object-contain bg-gray-900" />
        </div>
        <div>
          <p className="text-xs text-center text-gray-400 py-1">Grad-CAM</p>
          <img src={`data:image/jpeg;base64,${patient.heatmap}`}
            alt="heatmap" className="w-full max-h-32 object-contain bg-gray-900" />
        </div>
      </div>

      {/* Findings */}
      <div className="px-4 py-3">
        <p className="text-xs font-semibold text-gray-600 mb-1">AI Findings:</p>
        <ul className="space-y-0.5">
          {(patient.findings || []).map((f, i) => (
            <li key={i} className="text-xs text-gray-600 flex gap-1">
              <span className="text-blue-400 font-bold">{i + 1}.</span>{f}
            </li>
          ))}
        </ul>
      </div>

      <div className="px-4 pb-3 text-xs text-gray-400">
        Processing: {patient.processing_time_ms}ms
      </div>
    </div>
  );
}
