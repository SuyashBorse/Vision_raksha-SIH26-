// src/components/ImageCapture.jsx
// Drag-drop upload + live camera capture
// Spec: PRD FR-001, FR-002, US-001, US-002

import { useState, useRef, useCallback } from "react";
import { Camera, Upload, X } from "lucide-react";

export default function ImageCapture({ onImageReady, disabled }) {
  const [preview, setPreview]     = useState(null);
  const [dragOver, setDragOver]   = useState(false);
  const [cameraOn, setCameraOn]   = useState(false);
  const [error, setError]         = useState(null);

  const fileInputRef = useRef();
  const videoRef     = useRef();
  const streamRef    = useRef();

  // ── File pick / drag-drop ──────────────────────────────
  const handleFile = useCallback((file) => {
    setError(null);
    if (!file) return;

    const allowed = ["image/jpeg", "image/png", "image/webp"];
    if (!allowed.includes(file.type)) {
      setError("Only JPEG, PNG, or WEBP images are allowed.");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError("File too large — maximum 10 MB.");
      return;
    }

    const url = URL.createObjectURL(file);
    setPreview(url);
    onImageReady(file);
  }, [onImageReady]);

  const onDrop = (e) => {
    e.preventDefault(); setDragOver(false);
    handleFile(e.dataTransfer.files[0]);
  };

  // ── Camera capture ─────────────────────────────────────
  const startCamera = async () => {
    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment", width: 640, height: 480 }
      });
      streamRef.current = stream;
      videoRef.current.srcObject = stream;
      setCameraOn(true);
    } catch {
      setError("Camera not available — please upload an image instead.");
    }
  };

  const capturePhoto = () => {
    const canvas = document.createElement("canvas");
    canvas.width  = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext("2d").drawImage(videoRef.current, 0, 0);
    canvas.toBlob((blob) => {
      const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
      const url  = URL.createObjectURL(blob);
      setPreview(url);
      onImageReady(file);
      stopCamera();
    }, "image/jpeg", 0.9);
  };

  const stopCamera = () => {
    streamRef.current?.getTracks().forEach(t => t.stop());
    setCameraOn(false);
  };

  const reset = () => {
    setPreview(null); setError(null); stopCamera();
    onImageReady(null);
  };

  // ── Camera view ────────────────────────────────────────
  if (cameraOn) return (
    <div className="space-y-3">
      <div className="relative rounded-xl overflow-hidden bg-black aspect-video">
        <video ref={videoRef} autoPlay playsInline className="w-full h-full object-cover" />
        <div className="absolute bottom-0 inset-x-0 flex justify-center gap-4 p-4 bg-gradient-to-t from-black/60">
          <button onClick={capturePhoto}
            className="bg-white text-blue-700 font-bold px-6 py-2 rounded-full shadow hover:bg-blue-50 transition">
            Capture
          </button>
          <button onClick={stopCamera}
            className="bg-white/20 text-white px-4 py-2 rounded-full hover:bg-white/30 transition">
            Cancel
          </button>
        </div>
      </div>
    </div>
  );

  // ── Preview ────────────────────────────────────────────
  if (preview) return (
    <div className="space-y-3">
      <div className="relative rounded-xl overflow-hidden border-2 border-blue-300">
        <img src={preview} alt="Selected retinal image"
          className="w-full max-h-64 object-contain bg-gray-900" />
        <button onClick={reset}
          className="absolute top-2 right-2 bg-white/90 rounded-full p-1.5 shadow hover:bg-red-50 transition">
          <X size={16} className="text-gray-600" />
        </button>
      </div>
      <p className="text-xs text-center text-gray-500">
        Image ready for analysis — click <strong>Analyse</strong> below
      </p>
    </div>
  );

  // ── Default upload UI ──────────────────────────────────
  return (
    <div className="space-y-3">
      {/* Drag-drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => fileInputRef.current.click()}
        className={`
          border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition
          ${dragOver
            ? "border-blue-500 bg-blue-50"
            : "border-gray-300 hover:border-blue-400 hover:bg-blue-50/40"}
        `}
      >
        <Upload className="mx-auto mb-3 text-blue-400" size={36} />
        <p className="font-medium text-gray-700">Drop retinal image here</p>
        <p className="text-sm text-gray-400 mt-1">or click to browse · JPEG/PNG/WEBP · max 10MB</p>
        <input
          ref={fileInputRef} type="file"
          accept="image/jpeg,image/png,image/webp"
          className="hidden"
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </div>

      {/* Camera button */}
      <button onClick={startCamera} disabled={disabled}
        className="w-full flex items-center justify-center gap-2 border border-blue-300 text-blue-700
                   py-2.5 rounded-lg hover:bg-blue-50 transition text-sm font-medium disabled:opacity-50">
        <Camera size={16} /> Use Camera
      </button>

      {error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
          {error}
        </p>
      )}
    </div>
  );
}
