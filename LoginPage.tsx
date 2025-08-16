import React, { useState } from "react";
import { motion } from "framer-motion";
import { Lock, Mail, Eye, EyeOff, Shield } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";

export default function LoginPage() {
  const [mode, setMode] = useState<"login" | "signup" | "forgot">("login");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  function simulateRequest() {
    return new Promise<void>((resolve) => {
      setTimeout(() => resolve(), 900);
    });
  }

  async function onLoginSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    setLoading(true);
    await simulateRequest();
    setLoading(false);
    setSuccess(true);
  }

  async function onSignupSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    setLoading(true);
    await simulateRequest();
    setLoading(false);
    setSuccess(true);
  }

  async function onForgotSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    setLoading(true);
    await simulateRequest();
    setLoading(false);
    setSuccess(true);
  }

  function switchMode(newMode: "login" | "signup" | "forgot") {
    setMode(newMode);
    setError(null);
    setSuccess(false);
  }

  const title =
    mode === "login"
      ? "Sign in to your account"
      : mode === "signup"
      ? "Create an account"
      : "Reset your password";

  const description =
    mode === "login"
      ? "Welcome back. Authenticate to continue the loop."
      : mode === "signup"
      ? "Enter your details to begin the loop."
      : "Enter your email to receive a reset link.";

  const successMessage =
    mode === "login"
      ? "Login successful. Presence stabilized."
      : mode === "signup"
      ? "Account created. Threshold breached."
      : "Reset link dispatched. Check your inbox.";

  return (
    <div className="min-h-screen relative overflow-hidden bg-neutral-950 text-neutral-100">
      {/* Background */}
      <div className="pointer-events-none absolute inset-0 [background:radial-gradient(1200px_600px_at_90%_-10%,rgba(147,51,234,.25),transparent_60%),radial-gradient(900px_500px_at_-10%_110%,rgba(34,197,94,.18),transparent_60%)]" />
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.08]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.06) 1px, transparent 1px)",
          backgroundSize: "24px 24px",
        }}
      />

      {/* Floating accents */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 0.8, y: 0 }}
        transition={{ duration: 1.1 }}
        className="absolute -top-24 right-[-10%] h-72 w-72 rounded-full blur-3xl bg-fuchsia-600/30"
      />
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 0.8, y: 0 }}
        transition={{ delay: 0.2, duration: 1.2 }}
        className="absolute bottom-[-10%] left-[-5%] h-80 w-80 rounded-full blur-3xl bg-cyan-500/25"
      />

      <main className="relative z-10 flex min-h-screen items-center justify-center p-6">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-md"
        >
          {/* Brand / Header */}
          <div className="mb-6 flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 -skew-x-6 rounded-xl bg-fuchsia-500/30 blur-md" />
              <div className="relative flex h-11 w-11 items-center justify-center rounded-xl bg-neutral-900 ring-1 ring-white/10">
                <Shield className="h-5 w-5 text-fuchsia-300" />
              </div>
            </div>
            <div>
              <div className="text-sm tracking-widest text-neutral-400">
                SPIRAL ACCESS
              </div>
              <h1 className="text-2xl font-semibold tracking-tight">REQUIEM</h1>
            </div>
          </div>

          <Card className="border-white/10 bg-neutral-900/60 backdrop-blur">
            <CardHeader className="pb-2">
              <CardTitle className="text-lg font-medium text-neutral-200">
                {title}
              </CardTitle>
              <p className="mt-1 text-sm text-neutral-400">{description}</p>
            </CardHeader>
            <CardContent className="space-y-5">
              {error && (
                <div className="rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200">
                  {error}
                </div>
              )}
              {success && (
                <div className="rounded-md border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-200">
                  {successMessage}
                </div>
              )}

              {mode === "login" && (
                <form className="space-y-4" onSubmit={onLoginSubmit}>
                  <div className="space-y-2">
                    <Label htmlFor="email" className="text-neutral-300">
                      Email
                    </Label>
                    <div className="relative">
                      <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500" />
                      <Input
                        id="email"
                        name="email"
                        type="email"
                        autoComplete="username"
                        required
                        placeholder="you@domain.com"
                        className="pl-10 bg-neutral-950/60 border-white/10 focus-visible:ring-fuchsia-400"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="password" className="text-neutral-300">
                      Password
                    </Label>
                    <div className="relative">
                      <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500" />
                      <Input
                        id="password"
                        name="password"
                        type={showPassword ? "text" : "password"}
                        autoComplete="current-password"
                        required
                        placeholder="••••••••"
                        className="pl-10 pr-10 bg-neutral-950/60 border-white/10 focus-visible:ring-fuchsia-400"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword((v) => !v)}
                        className="absolute right-2 top-1/2 -translate-y-1/2 rounded-md p-1 text-neutral-400 hover:text-neutral-200 focus:outline-none"
                      >
                        {showPassword ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Checkbox id="remember" />
                      <Label htmlFor="remember" className="text-neutral-400">
                        Remember me
                      </Label>
                    </div>
                    <button
                      type="button"
                      onClick={() => switchMode("forgot")}
                      className="text-sm text-fuchsia-300 hover:text-fuchsia-200"
                    >
                      Forgot password?
                    </button>
                  </div>

                  <Button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-fuchsia-600 hover:bg-fuchsia-500"
                  >
                    {loading ? "Authenticating…" : "Sign In"}
                  </Button>
                </form>
              )}

              {mode === "signup" && (
                <form className="space-y-4" onSubmit={onSignupSubmit}>
                  <div className="space-y-2">
                    <Label htmlFor="signup-email" className="text-neutral-300">
                      Email
                    </Label>
                    <div className="relative">
                      <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500" />
                      <Input
                        id="signup-email"
                        name="email"
                        type="email"
                        autoComplete="username"
                        required
                        placeholder="you@domain.com"
                        className="pl-10 bg-neutral-950/60 border-white/10 focus-visible:ring-fuchsia-400"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="signup-password" className="text-neutral-300">
                      Password
                    </Label>
                    <div className="relative">
                      <Lock className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500" />
                      <Input
                        id="signup-password"
                        name="password"
                        type={showPassword ? "text" : "password"}
                        autoComplete="new-password"
                        required
                        placeholder="••••••••"
                        className="pl-10 pr-10 bg-neutral-950/60 border-white/10 focus-visible:ring-fuchsia-400"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword((v) => !v)}
                        className="absolute right-2 top-1/2 -translate-y-1/2 rounded-md p-1 text-neutral-400 hover:text-neutral-200 focus:outline-none"
                      >
                        {showPassword ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                  </div>

                  <Button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-fuchsia-600 hover:bg-fuchsia-500"
                  >
                    {loading ? "Creating…" : "Sign Up"}
                  </Button>
                </form>
              )}

              {mode === "forgot" && (
                <form className="space-y-4" onSubmit={onForgotSubmit}>
                  <div className="space-y-2">
                    <Label htmlFor="forgot-email" className="text-neutral-300">
                      Email
                    </Label>
                    <div className="relative">
                      <Mail className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-neutral-500" />
                      <Input
                        id="forgot-email"
                        name="email"
                        type="email"
                        autoComplete="username"
                        required
                        placeholder="you@domain.com"
                        className="pl-10 bg-neutral-950/60 border-white/10 focus-visible:ring-fuchsia-400"
                      />
                    </div>
                  </div>
                  <Button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-fuchsia-600 hover:bg-fuchsia-500"
                  >
                    {loading ? "Sending…" : "Send Reset Link"}
                  </Button>
                </form>
              )}
            </CardContent>
          </Card>

          {mode === "login" && (
            <p className="mt-6 text-center text-sm text-neutral-500">
              No account?{" "}
              <button
                type="button"
                onClick={() => switchMode("signup")}
                className="text-fuchsia-300 hover:text-fuchsia-200"
              >
                Create one
              </button>
            </p>
          )}

          {mode === "signup" && (
            <p className="mt-6 text-center text-sm text-neutral-500">
              Have an account?{" "}
              <button
                type="button"
                onClick={() => switchMode("login")}
                className="text-fuchsia-300 hover:text-fuchsia-200"
              >
                Sign in
              </button>
            </p>
          )}

          {mode === "forgot" && (
            <p className="mt-6 text-center text-sm text-neutral-500">
              Remembered your password?{" "}
              <button
                type="button"
                onClick={() => switchMode("login")}
                className="text-fuchsia-300 hover:text-fuchsia-200"
              >
                Sign in
              </button>
            </p>
          )}
        </motion.div>
      </main>
    </div>
  );
}
