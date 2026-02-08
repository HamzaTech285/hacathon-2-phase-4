import { useState, useEffect } from "react";
import { useToast } from "@/hooks/use-toast";
import { taskService, Task as BackendTask } from "@/services/api";

export type Priority = "low" | "medium" | "high";
export type RecurringFrequency = "daily" | "weekly" | "monthly";

export interface TodoFilters {
  search: string;
  priority: Priority | "all";
  category: string | "all";
  status: "all" | "completed" | "pending";
  sortBy: "created_at" | "due_date" | "priority" | "title";
  sortOrder: "asc" | "desc";
}

// Define our own Todo type that matches the backend but extends functionality
export interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string;
  user_id: number;
  created_at: string;
  updated_at: string;
  priority?: Priority;
  category_id?: string;
  is_recurring?: boolean;
  recurring_frequency?: RecurringFrequency;
  reminder_enabled?: boolean;
  completed_at?: string;
  due_time?: string;
}

// Define Category type
export interface Category {
  id: string;
  name: string;
  color: string;
  user_id: string;
}

export function useTodos() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<TodoFilters>({
    search: "",
    priority: "all",
    category: "all",
    status: "all",
    sortBy: "created_at",
    sortOrder: "desc",
  });
  const { toast } = useToast();

  const fetchTodos = async () => {
    try {
      const backendTasks = await taskService.getAllTasks();
      // Convert backend tasks to our Todo format
      const convertedTodos: Todo[] = backendTasks.map(task => ({
        id: task.id,
        title: task.title,
        description: task.description,
        completed: task.is_completed,
        due_date: task.due_date || undefined,
        user_id: task.user_id,
        created_at: task.created_at,
        updated_at: task.updated_at,
        priority: "medium", // Default priority
        category_id: undefined,
        is_recurring: false,
        recurring_frequency: undefined,
        reminder_enabled: false,
        completed_at: task.is_completed ? task.updated_at : undefined,
        due_time: undefined
      }));
      setTodos(convertedTodos);
    } catch (error) {
      console.error("Error fetching tasks:", error);
      toast({ 
        title: "Error fetching tasks", 
        description: "Could not load tasks from server", 
        variant: "destructive" 
      });
    }
  };

  const fetchCategories = async () => {
    // For now, return empty categories since backend doesn't support them
    setCategories([]);
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchTodos(), fetchCategories()]);
      setLoading(false);
    };
    loadData();
  }, []);

  const addTodo = async (todo: Omit<Todo, "id" | "completed" | "user_id" | "created_at" | "updated_at">) => {
    try {
      // Get user ID from token or store - for now using a placeholder
      const userId = 1; // This should come from authentication
      
      const taskData: BackendTask = {
        id: 0, // Will be assigned by backend
        title: todo.title,
        description: todo.description,
        is_completed: false,
        due_date: todo.due_date || undefined,
        user_id: userId,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      const newTask = await taskService.createTask({
        title: todo.title,
        description: todo.description,
        is_completed: false,
        due_date: todo.due_date || undefined,
        user_id: userId
      });

      // Convert to our Todo format
      const newTodo: Todo = {
        id: newTask.id,
        title: newTask.title,
        description: newTask.description,
        completed: newTask.is_completed,
        due_date: newTask.due_date || undefined,
        user_id: newTask.user_id,
        created_at: newTask.created_at,
        updated_at: newTask.updated_at,
        priority: todo.priority || "medium",
        category_id: todo.category_id,
        is_recurring: todo.is_recurring,
        recurring_frequency: todo.recurring_frequency,
        reminder_enabled: todo.reminder_enabled,
        completed_at: newTask.is_completed ? newTask.updated_at : undefined,
        due_time: todo.due_time
      };

      setTodos((prev) => [newTodo, ...prev]);
      toast({ title: "Task created", description: "Your task has been added" });
      return newTodo;
    } catch (error) {
      console.error("Error creating task:", error);
      toast({ 
        title: "Error creating task", 
        description: "Could not create task on server", 
        variant: "destructive" 
      });
      return null;
    }
  };

  const updateTodo = async (id: number, updates: Partial<Todo>) => {
    try {
      const todo = todos.find(t => t.id === id);
      if (!todo) return null;

      const taskUpdates = {
        title: updates.title,
        description: updates.description,
        is_completed: updates.completed,
        due_date: updates.due_date
      };

      const updatedTask = await taskService.updateTask(id, taskUpdates);

      const updatedTodo: Todo = {
        ...todo,
        ...updates,
        title: updates.title ?? todo.title,
        description: updates.description ?? todo.description,
        completed: updates.completed ?? todo.completed,
        due_date: updates.due_date ?? todo.due_date,
        updated_at: updatedTask.updated_at
      };

      setTodos((prev) => prev.map((t) => (t.id === id ? updatedTodo : t)));
      return updatedTodo;
    } catch (error) {
      console.error("Error updating task:", error);
      toast({ 
        title: "Error updating task", 
        description: "Could not update task on server", 
        variant: "destructive" 
      });
      return null;
    }
  };

  const toggleComplete = async (id: number) => {
    const todo = todos.find((t) => t.id === id);
    if (!todo) return;

    const completed = !todo.completed;
    const updates: Partial<Todo> = {
      completed,
      completed_at: completed ? new Date().toISOString() : undefined
    };

    // Handle recurring tasks
    if (completed && todo.is_recurring && todo.recurring_frequency) {
      const newDueDate = calculateNextDueDate(todo.due_date, todo.recurring_frequency);

      // Create new recurring task
      await addTodo({
        title: todo.title,
        description: todo.description,
        priority: todo.priority,
        category_id: todo.category_id,
        due_date: newDueDate,
        due_time: todo.due_time,
        is_recurring: true,
        recurring_frequency: todo.recurring_frequency,
        reminder_enabled: todo.reminder_enabled,
      });
    }

    await updateTodo(id, updates);
  };

  const deleteTodo = async (id: number) => {
    try {
      await taskService.deleteTask(id);
      setTodos((prev) => prev.filter((t) => t.id !== id));
      toast({ title: "Task deleted", description: "Your task has been removed" });
      return true;
    } catch (error) {
      console.error("Error deleting task:", error);
      toast({ 
        title: "Error deleting task", 
        description: "Could not delete task on server", 
        variant: "destructive" 
      });
      return false;
    }
  };

  const addCategory = async (name: string, color: string) => {
    // Backend doesn't support categories yet, so we'll simulate
    const newCategory: Category = {
      id: Math.random().toString(36).substring(7),
      name,
      color,
      user_id: "1" // Placeholder
    };
    setCategories((prev) => [...prev, newCategory]);
    return newCategory;
  };

  const filteredTodos = todos.filter((todo) => {
    if (filters.search && !todo.title.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    if (filters.priority !== "all" && todo.priority !== filters.priority) {
      return false;
    }
    if (filters.category !== "all" && todo.category_id !== filters.category) {
      return false;
    }
    if (filters.status === "completed" && !todo.completed) {
      return false;
    }
    if (filters.status === "pending" && todo.completed) {
      return false;
    }
    return true;
  });

  const sortedTodos = [...filteredTodos].sort((a, b) => {
    const order = filters.sortOrder === "asc" ? 1 : -1;

    switch (filters.sortBy) {
      case "title":
        return a.title.localeCompare(b.title) * order;
      case "priority": {
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        return (priorityOrder[a.priority || "medium"] - priorityOrder[b.priority || "medium"]) * order;
      }
      case "due_date":
        if (!a.due_date) return 1;
        if (!b.due_date) return -1;
        return (new Date(a.due_date).getTime() - new Date(b.due_date).getTime()) * order;
      default:
        return (new Date(a.created_at).getTime() - new Date(b.created_at).getTime()) * order;
    }
  });

  return {
    todos: sortedTodos,
    categories,
    loading,
    filters,
    setFilters,
    addTodo,
    updateTodo,
    toggleComplete,
    deleteTodo,
    addCategory,
    refetch: () => Promise.all([fetchTodos(), fetchCategories()]),
  };
}

function calculateNextDueDate(currentDueDate: string | null, frequency: RecurringFrequency): string {
  const base = currentDueDate ? new Date(currentDueDate) : new Date();

  switch (frequency) {
    case "daily":
      base.setDate(base.getDate() + 1);
      break;
    case "weekly":
      base.setDate(base.getDate() + 7);
      break;
    case "monthly":
      base.setMonth(base.getMonth() + 1);
      break;
  }

  return base.toISOString();
}