import { useState } from "react";
import { format } from "date-fns";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Pencil, Trash2, Clock, Repeat, Bell, Calendar } from "lucide-react";
import { cn } from "@/lib/utils";
import { Todo, Category } from "@/hooks/useTodos";

interface TodoItemProps {
  todo: Todo;
  categories: Category[];
  onToggle: (id: number) => void;
  onEdit: (todo: Todo) => void;
  onDelete: (id: number) => void;
}

const priorityColors = {
  high: "bg-red-500/20 text-red-400 border-red-500/30",
  medium: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
  low: "bg-green-500/20 text-green-400 border-green-500/30",
};

export function TodoItem({ todo, categories, onToggle, onEdit, onDelete }: TodoItemProps) {
  const [isHovered, setIsHovered] = useState(false);
  const category = categories.find((c) => c.id === todo.category_id);
  const priority = todo.priority || "medium";

  const isOverdue = todo.due_date && new Date(todo.due_date) < new Date() && !todo.completed;

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={cn(
        "group p-4 rounded-xl border transition-all duration-300",
        todo.completed
          ? "bg-muted/30 border-border opacity-60"
          : "bg-card/50 border-border hover:border-primary/50 hover:neon-glow",
        isOverdue && !todo.completed && "border-destructive/50"
      )}
    >
      <div className="flex items-start gap-4">
        {/* Checkbox */}
        <div className="pt-1">
          <Checkbox
            checked={todo.completed}
            onCheckedChange={() => onToggle(todo.id)}
            className={cn(
              "w-5 h-5 border-2 transition-all",
              todo.completed
                ? "bg-primary border-primary"
                : "border-muted-foreground hover:border-primary"
            )}
          />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <h3
              className={cn(
                "font-medium text-foreground transition-all",
                todo.completed && "line-through text-muted-foreground"
              )}
            >
              {todo.title}
            </h3>

            {/* Priority Badge */}
            <Badge variant="outline" className={cn("text-xs", priorityColors[priority])}>
              {priority}
            </Badge>

            {/* Category Badge */}
            {category && (
              <Badge
                variant="outline"
                className="text-xs"
                style={{
                  backgroundColor: `${category.color}20`,
                  color: category.color,
                  borderColor: `${category.color}50`,
                }}
              >
                {category.name}
              </Badge>
            )}

            {/* Recurring Icon */}
            {todo.is_recurring && (
              <Repeat className="w-3.5 h-3.5 text-primary" />
            )}

            {/* Reminder Icon */}
            {todo.reminder_enabled && (
              <Bell className="w-3.5 h-3.5 text-secondary" />
            )}
          </div>

          {/* Description */}
          {todo.description && (
            <p className="text-sm text-muted-foreground mb-2 line-clamp-2">
              {todo.description}
            </p>
          )}

          {/* Due Date */}
          {todo.due_date && (
            <div
              className={cn(
                "flex items-center gap-1.5 text-xs",
                isOverdue && !todo.completed ? "text-destructive" : "text-muted-foreground"
              )}
            >
              <Calendar className="w-3.5 h-3.5" />
              <span>{format(new Date(todo.due_date), "MMM d, yyyy")}</span>
              {todo.due_time && (
                <>
                  <Clock className="w-3.5 h-3.5 ml-2" />
                  <span>{todo.due_time}</span>
                </>
              )}
            </div>
          )}
        </div>

        {/* Actions */}
        <div
          className={cn(
            "flex items-center gap-1 transition-opacity",
            isHovered ? "opacity-100" : "opacity-0"
          )}
        >
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onEdit(todo)}
            className="h-8 w-8 text-muted-foreground hover:text-primary hover:bg-primary/10"
          >
            <Pencil className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onDelete(todo.id)}
            className="h-8 w-8 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
