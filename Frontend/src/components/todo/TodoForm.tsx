import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { CalendarIcon, X } from "lucide-react";
import { format } from "date-fns";
import { cn } from "@/lib/utils";
import { Todo, Category, Priority, RecurringFrequency } from "@/hooks/useTodos";

interface TodoFormProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: TodoFormData) => void;
  categories: Category[];
  editTodo?: Todo | null;
}

export interface TodoFormData {
  title: string;
  description: string;
  priority: Priority;
  category_id: string | null;
  due_date: string | null;
  due_time: string | null;
  is_recurring: boolean;
  recurring_frequency: RecurringFrequency | null;
  reminder_enabled: boolean;
}

export function TodoForm({ open, onClose, onSubmit, categories, editTodo }: TodoFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<Priority>("medium");
  const [categoryId, setCategoryId] = useState<string | null>(null);
  const [dueDate, setDueDate] = useState<Date | undefined>();
  const [dueTime, setDueTime] = useState("");
  const [isRecurring, setIsRecurring] = useState(false);
  const [recurringFrequency, setRecurringFrequency] = useState<RecurringFrequency>("weekly");
  const [reminderEnabled, setReminderEnabled] = useState(false);

  useEffect(() => {
    if (editTodo) {
      setTitle(editTodo.title);
      setDescription(editTodo.description || "");
      setPriority(editTodo.priority);
      setCategoryId(editTodo.category_id);
      setDueDate(editTodo.due_date ? new Date(editTodo.due_date) : undefined);
      setDueTime(editTodo.due_time || "");
      setIsRecurring(editTodo.is_recurring);
      setRecurringFrequency(editTodo.recurring_frequency || "weekly");
      setReminderEnabled(editTodo.reminder_enabled);
    } else {
      resetForm();
    }
  }, [editTodo, open]);

  const resetForm = () => {
    setTitle("");
    setDescription("");
    setPriority("medium");
    setCategoryId(null);
    setDueDate(undefined);
    setDueTime("");
    setIsRecurring(false);
    setRecurringFrequency("weekly");
    setReminderEnabled(false);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    onSubmit({
      title: title.trim(),
      description: description.trim(),
      priority,
      category_id: categoryId,
      due_date: dueDate ? dueDate.toISOString() : null,
      due_time: dueTime || null,
      is_recurring: isRecurring,
      recurring_frequency: isRecurring ? recurringFrequency : null,
      reminder_enabled: reminderEnabled,
    });

    resetForm();
    onClose();
  };

  return (
    <Dialog open={open} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-lg bg-card border-border">
        <DialogHeader>
          <DialogTitle className="text-foreground">
            {editTodo ? "Edit Task" : "Create New Task"}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Title */}
          <div className="space-y-2">
            <Label htmlFor="title">Title *</Label>
            <Input
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="What needs to be done?"
              className="bg-input border-border focus:border-primary"
              required
            />
          </div>

          {/* Description */}
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add more details..."
              className="bg-input border-border focus:border-primary resize-none"
              rows={3}
            />
          </div>

          {/* Priority & Category Row */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Priority</Label>
              <Select value={priority} onValueChange={(v) => setPriority(v as Priority)}>
                <SelectTrigger className="bg-input border-border">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="high">🔴 High</SelectItem>
                  <SelectItem value="medium">🟡 Medium</SelectItem>
                  <SelectItem value="low">🟢 Low</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Category</Label>
              <Select value={categoryId || "none"} onValueChange={(v) => setCategoryId(v === "none" ? null : v)}>
                <SelectTrigger className="bg-input border-border">
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="none">No Category</SelectItem>
                  {categories.map((cat) => (
                    <SelectItem key={cat.id} value={cat.id}>
                      <span className="flex items-center gap-2">
                        <span
                          className="w-2 h-2 rounded-full"
                          style={{ backgroundColor: cat.color || "#22C55E" }}
                        />
                        {cat.name}
                      </span>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Due Date & Time */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Due Date</Label>
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="outline"
                    className={cn(
                      "w-full justify-start text-left font-normal bg-input border-border",
                      !dueDate && "text-muted-foreground"
                    )}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {dueDate ? format(dueDate, "PPP") : "Pick a date"}
                    {dueDate && (
                      <X
                        className="ml-auto h-4 w-4 hover:text-destructive"
                        onClick={(e) => {
                          e.stopPropagation();
                          setDueDate(undefined);
                        }}
                      />
                    )}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={dueDate}
                    onSelect={setDueDate}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
            </div>

            <div className="space-y-2">
              <Label htmlFor="dueTime">Due Time</Label>
              <Input
                id="dueTime"
                type="time"
                value={dueTime}
                onChange={(e) => setDueTime(e.target.value)}
                className="bg-input border-border"
              />
            </div>
          </div>

          {/* Recurring Toggle */}
          <div className="flex items-center justify-between p-4 rounded-lg border border-border bg-muted/30">
            <div className="space-y-0.5">
              <Label className="text-foreground">Recurring Task</Label>
              <p className="text-xs text-muted-foreground">Automatically reschedule when completed</p>
            </div>
            <Switch
              checked={isRecurring}
              onCheckedChange={setIsRecurring}
            />
          </div>

          {/* Recurring Frequency */}
          {isRecurring && (
            <div className="space-y-2">
              <Label>Repeat Every</Label>
              <Select value={recurringFrequency} onValueChange={(v) => setRecurringFrequency(v as RecurringFrequency)}>
                <SelectTrigger className="bg-input border-border">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="daily">Daily</SelectItem>
                  <SelectItem value="weekly">Weekly</SelectItem>
                  <SelectItem value="monthly">Monthly</SelectItem>
                </SelectContent>
              </Select>
            </div>
          )}

          {/* Reminder Toggle */}
          <div className="flex items-center justify-between p-4 rounded-lg border border-border bg-muted/30">
            <div className="space-y-0.5">
              <Label className="text-foreground">Enable Reminder</Label>
              <p className="text-xs text-muted-foreground">Get notified when the task is due</p>
            </div>
            <Switch
              checked={reminderEnabled}
              onCheckedChange={setReminderEnabled}
            />
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" className="bg-primary hover:bg-primary/90">
              {editTodo ? "Save Changes" : "Create Task"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
