import { CheckCircle2, Clock, AlertTriangle, ListTodo } from "lucide-react";
import { Todo } from "@/hooks/useTodos";

interface TodoStatsProps {
  todos: Todo[];
}

export function TodoStats({ todos }: TodoStatsProps) {
  const total = todos.length;
  const completed = todos.filter((t) => t.completed).length;
  const pending = total - completed;
  const overdue = todos.filter(
    (t) => !t.completed && t.due_date && new Date(t.due_date) < new Date()
  ).length;
  const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;

  const stats = [
    {
      label: "Total Tasks",
      value: total,
      icon: ListTodo,
      color: "text-primary",
      bgColor: "bg-primary/10",
    },
    {
      label: "Completed",
      value: completed,
      icon: CheckCircle2,
      color: "text-green-400",
      bgColor: "bg-green-500/10",
    },
    {
      label: "Pending",
      value: pending,
      icon: Clock,
      color: "text-yellow-400",
      bgColor: "bg-yellow-500/10",
    },
    {
      label: "Overdue",
      value: overdue,
      icon: AlertTriangle,
      color: "text-red-400",
      bgColor: "bg-red-500/10",
    },
  ];

  return (
    <div className="space-y-4">
      {/* Progress Bar */}
      <div className="p-4 rounded-xl border border-border bg-card/50">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm text-muted-foreground">Completion Rate</span>
          <span className="text-lg font-bold text-primary neon-text">{completionRate}%</span>
        </div>
        <div className="h-2 bg-muted rounded-full overflow-hidden">
          <div
            className="h-full bg-primary transition-all duration-500 rounded-full"
            style={{ width: `${completionRate}%` }}
          />
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-3">
        {stats.map((stat) => (
          <div
            key={stat.label}
            className="p-4 rounded-xl border border-border bg-card/50 hover:border-primary/30 transition-all"
          >
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                <stat.icon className={`w-5 h-5 ${stat.color}`} />
              </div>
              <div>
                <p className="text-2xl font-bold text-foreground">{stat.value}</p>
                <p className="text-xs text-muted-foreground">{stat.label}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
