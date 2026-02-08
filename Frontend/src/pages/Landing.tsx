import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Zap, Bell, Repeat, Filter, Tag } from "lucide-react";

const features = [
  { icon: CheckCircle2, title: "Task Management", desc: "Create, edit, and organize your tasks" },
  { icon: Tag, title: "Categories & Tags", desc: "Organize with custom categories" },
  { icon: Filter, title: "Smart Filters", desc: "Search, filter, and sort tasks" },
  { icon: Zap, title: "Priorities", desc: "Set high, medium, or low priority" },
  { icon: Bell, title: "Reminders", desc: "Never miss a deadline" },
  { icon: Repeat, title: "Recurring Tasks", desc: "Auto-schedule repeating tasks" },
];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Matrix-style background effect */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-primary/5" />
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute text-primary/20 text-xs font-mono"
            style={{
              left: `${Math.random() * 100}%`,
              top: `-20px`,
              animation: `matrix-rain ${5 + Math.random() * 10}s linear infinite`,
              animationDelay: `${Math.random() * 5}s`,
            }}
          >
            {Math.random() > 0.5 ? "1" : "0"}
          </div>
        ))}
      </div>

      <div className="relative z-10 container mx-auto px-4 py-16 flex flex-col items-center justify-center min-h-screen">
        {/* Hero Section */}
        <div className="text-center max-w-4xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-primary/30 bg-primary/10 mb-8">
            <Zap className="w-4 h-4 text-primary" />
            <span className="text-sm text-primary font-medium">Powered by Matrix Green</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="text-foreground">Task </span>
            <span className="text-primary neon-text">Flow</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            The ultimate todo app with neon style. Organize your life with smart features, 
            beautiful design, and powerful productivity tools.
          </p>
          
          <Button
            onClick={() => navigate("/auth")}
            size="lg"
            className="px-12 py-6 text-lg font-semibold bg-primary hover:bg-primary/90 text-primary-foreground animate-pulse-glow transition-all duration-300 hover:scale-105"
          >
            Get Started
          </Button>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group p-6 rounded-xl border border-border bg-card/50 glass hover:border-primary/50 hover:neon-glow transition-all duration-300"
            >
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                <feature.icon className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">{feature.title}</h3>
              <p className="text-muted-foreground text-sm">{feature.desc}</p>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-16 text-center text-muted-foreground text-sm">
          <p>Built with 💚 using Matrix Green aesthetic</p>
        </div>
      </div>
    </div>
  );
}
