// src/pages/LoginPage.jsx — VisionRaksha Login Screen
import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { Eye, LogIn, AlertCircle } from "lucide-react";

export default function LoginPage() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
    } catch (err) {
      const msg = err.response?.data?.message || "Login failed. Please check your credentials.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const quickLogin = async (user, pass) => {
    setUsername(user);
    setPassword(pass);
    setError("");
    setLoading(true);
    try {
      await login(user, pass);
    } catch (err) {
      setError(err.response?.data?.message || "Login failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cover bg-center bg-no-repeat flex items-center justify-center p-4 relative overflow-hidden" style={{ backgroundImage: 'url(/bg_login.jpg)' }}>
      {/* Background overlay */}
      <div className="absolute inset-0 bg-[#1F2F42]/70 backdrop-blur-[2px] z-0" />

      {/* Background glow */}
      <div className="absolute top-20 left-1/4 w-96 h-96 bg-[#22AEB0]/20 rounded-full blur-3xl pointer-events-none z-0" />
      <div className="absolute bottom-20 right-1/4 w-80 h-80 bg-[#38C4C4]/20 rounded-full blur-3xl pointer-events-none z-0" />

      <div className="w-full max-w-md z-10">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="p-3.5 bg-[#22AEB0]/15 rounded-2xl backdrop-blur-md border border-[#22AEB0]/20 shadow-lg">
              <svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 24C4 24 12 10 24 10C36 10 44 24 44 24C44 24 36 38 24 38C12 38 4 24 4 24Z"
                  stroke="#22AEB0" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
                <circle cx="24" cy="24" r="7" stroke="#22AEB0" strokeWidth="2" fill="none" />
                <circle cx="24" cy="24" r="3" fill="#22AEB0" />
                <line x1="24" y1="17" x2="24" y2="14" stroke="#38C4C4" strokeWidth="1.5" strokeLinecap="round" />
                <line x1="24" y1="31" x2="24" y2="34" stroke="#38C4C4" strokeWidth="1.5" strokeLinecap="round" />
                <line x1="17" y1="24" x2="14" y2="24" stroke="#38C4C4" strokeWidth="1.5" strokeLinecap="round" />
                <line x1="31" y1="24" x2="34" y2="24" stroke="#38C4C4" strokeWidth="1.5" strokeLinecap="round" />
              </svg>
            </div>
            <div className="text-left">
              <h1 className="text-3xl font-bold text-white tracking-wide">
                Vision<span className="text-[#22AEB0]">Raksha</span>
              </h1>
              <p className="text-[#76D6D2] text-xs font-semibold uppercase tracking-wider">AI for Healthier Tomorrows</p>
            </div>
          </div>
          <p className="text-[#94A1AB] text-sm font-medium">
            Explainable AI for Diabetic Retinopathy Screening
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-8 border border-[#E1E9EC]">
          <h2 className="text-xl font-bold text-[#1F2F42] mb-6 text-center">
            Sign In to Dashboard
          </h2>

          {error && (
            <div className="mb-5 p-3.5 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2 text-sm text-rose-700 font-medium">
              <AlertCircle size={18} className="flex-shrink-0" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-[#657685] mb-1.5">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-themed"
                placeholder="Enter username"
                required
                autoFocus
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-[#657685] mb-1.5">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-themed"
                placeholder="Enter password"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3.5 text-sm gap-2 mt-2"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <LogIn size={18} />
                  Sign In
                </>
              )}
            </button>
          </form>

          {/* Quick Login for Demo */}
          <div className="mt-6 pt-6 border-t border-[#E1E9EC]">
            <p className="text-xs text-[#94A1AB] font-semibold text-center mb-3">
              Quick Persona Sign In
            </p>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => quickLogin("asha_demo", "asha123")}
                className="px-3 py-2.5 text-xs bg-[#E8F7F6] hover:bg-[#22AEB0]/15 text-[#22AEB0] rounded-xl border border-[#22AEB0]/20 font-semibold transition-all cursor-pointer"
              >
                👩‍⚕️ ASHA
              </button>
              <button
                onClick={() => quickLogin("doctor_demo", "doctor123")}
                className="px-3 py-2.5 text-xs bg-[#E8F7F6] hover:bg-[#22AEB0]/15 text-[#22AEB0] rounded-xl border border-[#22AEB0]/20 font-semibold transition-all cursor-pointer"
              >
                🩺 Doctor
              </button>
              <button
                onClick={() => quickLogin("admin", "admin123")}
                className="px-3 py-2.5 text-xs bg-[#E8F7F6] hover:bg-[#22AEB0]/15 text-[#22AEB0] rounded-xl border border-[#22AEB0]/20 font-semibold transition-all cursor-pointer"
              >
                🔧 Admin
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
