import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { Loader2, Mail, Lock, User, ArrowLeft } from "lucide-react";
import { z } from "zod";
import { authService } from "@/services/api";

const emailSchema = z.string().email("Please enter a valid email");
const passwordSchema = z.string().min(6, "Password must be at least 6 characters");

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  useEffect(() => {
    // Only auto-redirect if we have a token AND it's valid
    // But let's keep it simple: if they are on /auth, let them stay there unless they just logged in
    // This allows them to see the page first.
    const checkExistingAuth = async () => {
      if (authService.isAuthenticated()) {
        try {
          // Verify token is still good
          const response = await fetch('http://localhost:8000/health');
          if (response.ok) {
            // navigate("/dashboard"); // Optional: auto-redirect if already logged in
          }
        } catch (e) {
          authService.logout();
        }
      }
    };
    // checkExistingAuth(); 
  }, [navigate]);

  const validateForm = () => {
    try {
      emailSchema.parse(email);
    } catch (e) {
      if (e instanceof z.ZodError) {
        toast({ title: "Invalid email", description: e.errors[0].message, variant: "destructive" });
        return false;
      }
    }

    try {
      passwordSchema.parse(password);
    } catch (e) {
      if (e instanceof z.ZodError) {
        toast({ title: "Invalid password", description: e.errors[0].message, variant: "destructive" });
        return false;
      }
    }

    if (!isLogin && password !== confirmPassword) {
      toast({ title: "Passwords don't match", description: "Please make sure your passwords match", variant: "destructive" });
      return false;
    }

    return true;
  };

  const handleEmailAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      if (isLogin) {
        // Login with backend API
        await authService.login({ email, password });
        toast({ title: "Welcome back!", description: "Successfully logged in. Elevating you to your dashboard..." });
        // Stay hold for a moment for better UX
        setTimeout(() => {
          navigate("/dashboard");
        }, 1200);
      } else {
        // Register with backend API
        await authService.register({ email, password });
        toast({ title: "Account created!", description: "Welcome to TaskFlow! Preparing your personalized workspace..." });
        // Stay hold for a moment for better UX
        setTimeout(() => {
          navigate("/dashboard");
        }, 1200);
      }
    } catch (error: any) {
      console.error("Authentication error:", error);
      let errorMessage = "An error occurred during authentication";

      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }

      toast({
        title: "Authentication Error",
        description: errorMessage,
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleAuth = async () => {
    setGoogleLoading(true);
    toast({
      title: "Not Supported",
      description: "Google authentication is not supported with the custom backend. Please use email/password.",
      variant: "destructive"
    });
    setGoogleLoading(false);
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background glow effects */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/20 rounded-full blur-3xl" />

      <div className="w-full max-w-md relative z-10">
        {/* Back button */}
        <Button
          variant="ghost"
          onClick={() => navigate("/")}
          className="mb-6 text-muted-foreground hover:text-primary"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Home
        </Button>

        <div className="p-8 rounded-2xl border border-border bg-card/80 glass neon-border">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">
              <span className="text-primary neon-text">Task</span>Flow
            </h1>
            <p className="text-muted-foreground">
              {isLogin ? "Welcome back! Sign in to continue" : "Create your account to get started"}
            </p>
          </div>

          {/* Google Auth Button */}
          <Button
            onClick={handleGoogleAuth}
            disabled={googleLoading}
            variant="outline"
            className="w-full mb-6 py-6 border-border hover:border-primary hover:bg-primary/10 transition-all"
          >
            {googleLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <>
                <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                  <path
                    fill="currentColor"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="currentColor"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="currentColor"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  />
                  <path
                    fill="currentColor"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  />
                </svg>
                Continue with Google
              </>
            )}
          </Button>

          {/* Divider */}
          <div className="relative mb-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-border" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-card px-2 text-muted-foreground">Or continue with email</span>
            </div>
          </div>

          {/* Email Form */}
          <form onSubmit={handleEmailAuth} className="space-y-4">
            {!isLogin && (
              <div className="space-y-2">
                <Label htmlFor="fullName" className="text-foreground">Full Name</Label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    id="fullName"
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="John Doe"
                    className="pl-10 bg-input border-border focus:border-primary focus:ring-primary/20"
                  />
                </div>
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="email" className="text-foreground">Email</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  required
                  className="pl-10 bg-input border-border focus:border-primary focus:ring-primary/20"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-foreground">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  className="pl-10 bg-input border-border focus:border-primary focus:ring-primary/20"
                />
              </div>
            </div>

            {!isLogin && (
              <div className="space-y-2">
                <Label htmlFor="confirmPassword" className="text-foreground">Confirm Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    id="confirmPassword"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                    className="pl-10 bg-input border-border focus:border-primary focus:ring-primary/20"
                  />
                </div>
              </div>
            )}

            <Button
              type="submit"
              disabled={loading}
              className="w-full py-6 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold transition-all hover:neon-glow"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : isLogin ? (
                "Sign In"
              ) : (
                "Create Account"
              )}
            </Button>
          </form>

          {/* Toggle Login/Signup */}
          <div className="mt-6 text-center">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <span className="font-semibold text-primary">{isLogin ? "Sign Up" : "Sign In"}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
