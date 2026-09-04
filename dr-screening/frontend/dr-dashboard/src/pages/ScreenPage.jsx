// src/pages/ScreenPage.jsx
// Full screening flow: patient select → upload → analyse → result → validate
// Spec: PRD US-001 to US-009

import { useState, useEffect } from "react";
import { Loader2, UserPlus, WifiOff, Clock } from "lucide-react";
import ImageCapture   from "../components/ImageCapture";
import ResultSection  from "../components/ResultSection";
import { analyseImage, validateScreening, createPatient } from "../utils/api";
import { enqueueImage, getPendingCount } from "../utils/offlineQueue";


const STEPS = ["Patient", "Capture", "Result"];

export default function ScreenPage() {
  const [step, setStep]         = useState(0);
  const [patient, setPatient]   = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [result, setResult]     = useState(null);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState(null);
  const [queued, setQueued]     = useState(false);
  const [pendingCount, setPending] = useState(0);

  useEffect(() => {
    getPendingCount().then(setPending).catch(() => {});
  }, [queued]);


  // ── Step 0 — Patient quick-register ───────────────────
  const handlePatient = async (e) => {
    e.preventDefault();
    const fd   = new FormData(e.target);
    const data = { name: fd.get("name"), age: Number(fd.get("age")), gender: fd.get("gender") };
    try {
      const res = await createPatient(data);
      setPatient(res);
      setStep(1);
    } catch {
      // Continue without patient (optional)
      setPatient({ patient_id: null, name: fd.get("name") });
      setStep(1);
    }
  };

  // ── Step 1 — Analyse image ─────────────────────────────
  const handleAnalyse = async () => {
    if (!imageFile) return;
    setLoading(true); setError(null); setQueued(false);
    try {
      const data = await analyseImage(imageFile, patient?.patient_id);
      setResult(data);
      setStep(2);
    } catch (err) {
      // If offline → queue the image
      if (!navigator.onLine) {
        await enqueueImage({
          file: imageFile,
          patientId: patient?.patient_id,
          patientName: patient?.name || "Unknown",
        });
        setQueued(true);
        setError(null);
      } else {
        const msg = err.response?.data?.detail?.message
                 || err.response?.data?.message
                 || "Analysis failed — please try again";
        setError(msg);
      }
    } finally {
      setLoading(false);
    }
  };


  // ── Step 2 — Doctor validation ─────────────────────────
  const handleValidate = async ({ action, override_reason, note, screening_id }) => {
    try {
      await validateScreening(screening_id, {
        action, override_reason, note, doctor_id: "dr_demo"
      });
    } catch (err) {
      console.error("Validation error:", err);
    }
  };

  const reset = () => { setStep(0); setPatient(null); setImageFile(null); setResult(null); setError(null); };

  return (
    <div className="p-6 max-w-2xl mx-auto">

      {/* ── Step indicator ────────────────────────────── */}
      <div className="flex items-center gap-2 mb-6">
        {STEPS.map((label, i) => (
          <div key={label} className="flex items-center gap-2">
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold
              ${i < step  ? "bg-green-500 text-white"
              : i === step ? "bg-blue-700 text-white"
              : "bg-gray-200 text-gray-500"}`}>
              {i < step ? "✓" : i + 1}
            </div>
            <span className={`text-sm font-medium ${i === step ? "text-blue-700" : "text-gray-400"}`}>
              {label}
            </span>
            {i < STEPS.length - 1 && <div className="w-8 h-px bg-gray-200" />}
          </div>
        ))}
        {step > 0 && (
          <button onClick={reset} className="ml-auto text-xs text-gray-400 hover:text-red-500 transition">
            ↺ Start over
          </button>
        )}
      </div>

      {/* ── Step 0: Patient info ─────────────────────── */}
      {step === 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <div className="flex items-center gap-2 mb-4">
            <UserPlus size={20} className="text-blue-600" />
            <h2 className="font-semibold text-gray-700">Patient Information</h2>
          </div>
          <form onSubmit={handlePatient} className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-600">Full Name *</label>
              <input name="name" required placeholder="e.g. Ramesh Kumar"
                className="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-sm font-medium text-gray-600">Age *</label>
                <input name="age" type="number" required min="1" max="120" placeholder="52"
                  className="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300" />
              </div>
              <div>
                <label className="text-sm font-medium text-gray-600">Gender</label>
                <select name="gender"
                  className="mt-1 w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300">
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                  <option value="O">Other</option>
                </select>
              </div>
            </div>
            <button type="submit"
              className="w-full bg-blue-700 text-white py-2.5 rounded-lg text-sm font-semibold hover:bg-blue-800 transition">
              Continue to Image Capture →
            </button>
          </form>
          <button onClick={() => setStep(1)}
            className="w-full mt-2 text-gray-400 text-xs hover:text-gray-600 transition">
            Skip patient info (anonymous screening)
          </button>
        </div>
      )}

      {/* ── Step 1: Image capture ─────────────────────── */}
      {step === 1 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="font-semibold text-gray-700 mb-1">
            Capture Retinal Image
            {patient?.name && <span className="text-blue-600 font-normal"> — {patient.name}</span>}
          </h2>
          <p className="text-xs text-gray-400 mb-4">JPEG/PNG/WEBP · max 10MB · fundus photograph</p>

          <ImageCapture onImageReady={setImageFile} disabled={loading} />

          {error && (
            <div className="mt-3 bg-red-50 border border-red-200 rounded-lg px-3 py-2 text-sm text-red-700">
              {error}
            </div>
          )}

          {queued && (
            <div className="mt-3 bg-orange-50 border border-orange-200 rounded-lg px-3 py-2 text-sm text-orange-700 flex items-center gap-2">
              <WifiOff size={14} />
              <span>
                <strong>Saved offline.</strong> This image will be analysed automatically when you reconnect.
                {pendingCount > 0 && ` (${pendingCount} pending)`}
              </span>
            </div>
          )}

          {pendingCount > 0 && !queued && (
            <div className="mt-3 flex items-center gap-2 text-xs text-orange-600">
              <Clock size={12} /> {pendingCount} image{pendingCount > 1 ? "s" : ""} queued — will sync when online
            </div>
          )}


          <button
            onClick={handleAnalyse}
            disabled={!imageFile || loading}
            className="mt-4 w-full bg-blue-700 text-white py-3 rounded-lg text-sm font-bold
                       hover:bg-blue-800 disabled:opacity-40 disabled:cursor-not-allowed transition
                       flex items-center justify-center gap-2"
          >
            {loading
              ? <><Loader2 size={16} className="animate-spin" /> Analysing...</>
              : "🔬 Analyse Image"}
          </button>
        </div>
      )}

      {/* ── Step 2: Result ────────────────────────────── */}
      {step === 2 && result && (
        <ResultSection result={result} onValidate={handleValidate} />
      )}
    </div>
  );
}
