/** Dashboard Page Component */

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useTodos } from "@/hooks/useTodos";
import { TodoItem } from "@/components/todo/TodoItem";
import { TodoForm, TodoFormData } from "@/components/todo/TodoForm";
import { TodoFilters } from "@/components/todo/TodoFilters";
import { TodoStats } from "@/components/todo/TodoStats";
import { ChatPanel } from "@/components/chat/ChatPanel";
import { Plus, LogOut, Loader2, Zap, ListTodo, MessageCircle } from "lucide-react";
import { isAuthenticated, removeToken } from "../utils/auth";
import { Todo } from "@/hooks/useTodos";

export default function Dashboard() {
  const [showForm, setShowForm] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const navigate = useNavigate();
  const {
    todos,
    categories,
    loading,
    filters,
    setFilters,
    addTodo,
    updateTodo,
    toggleComplete,
    deleteTodo,
  } = useTodos();

  useEffect(() => {
    if (!isAuthenticated()) {
      navigate('/auth');
    }
  }, [navigate]);

  const handleSignOut = () => {
    removeToken();
    navigate('/auth');
  };

  const handleFormSubmit = async (data: TodoFormData) => {
    if (editingTodo) {
      await updateTodo(editingTodo.id, data);
    } else {
      await addTodo(data);
    }
    setEditingTodo(null);
  };

  const handleEdit = (todo: Todo) => {
    setEditingTodo(todo);
    setShowForm(true);
  };

  if (!isAuthenticated()) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-primary animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 sticky top-0 z-50 backdrop-blur-lg">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center">
              <Zap className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">
                <span className="text-primary neon-text">Task</span>Flow
              </h1>
              <p className="text-xs text-muted-foreground">Stay organized & productive</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button
              onClick={() => {
                setEditingTodo(null);
                setShowForm(true);
              }}
              className="bg-primary hover:bg-primary/90 text-primary-foreground gap-2"
            >
              <Plus className="w-4 h-4" />
              <span className="hidden sm:inline">New Task</span>
            </Button>
            <Button
              variant="outline"
              size="icon"
              onClick={handleSignOut}
              className="border-border hover:border-primary hover:bg-primary/10"
            >
              <LogOut className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar - Stats */}
          <aside className="lg:col-span-1">
            <TodoStats todos={todos} />
          </aside>

          {/* Main - Todo List */}
          <div className="lg:col-span-3 space-y-6">
            {/* Filters */}
            <TodoFilters
              filters={filters}
              onFiltersChange={setFilters}
              categories={categories}
            />

            {/* Todo List */}
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 text-primary animate-spin" />
              </div>
            ) : todos.length === 0 ? (
              <div className="text-center py-16 px-4">
                <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-6">
                  <ListTodo className="w-10 h-10 text-primary" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2">No tasks yet</h3>
                <p className="text-muted-foreground mb-6 max-w-sm mx-auto">
                  Create your first task to get started with organizing your day!
                </p>
                <Button
                  onClick={() => {
                    setEditingTodo(null);
                    setShowForm(true);
                  }}
                  className="bg-primary hover:bg-primary/90"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Create Your First Task
                </Button>
              </div>
            ) : (
              <div className="space-y-3">
                {todos.map((todo) => (
                  <TodoItem
                    key={todo.id}
                    todo={todo}
                    categories={categories}
                    onToggle={toggleComplete}
                    onEdit={handleEdit}
                    onDelete={deleteTodo}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Todo Form Modal */}
      <TodoForm
        open={showForm}
        onClose={() => {
          setShowForm(false);
          setEditingTodo(null);
        }}
        onSubmit={handleFormSubmit}
        categories={categories}
        editTodo={editingTodo}
      />

      {/* Chat Panel */}
      <ChatPanel isOpen={showChat} onClose={() => setShowChat(false)} />

      {/* Floating Chatbot Button */}
      <Button
        size="icon"
        title="Chat"
        aria-label="Open chat"
        style={{
          bottom: "calc(1.5rem + env(safe-area-inset-bottom))",
          right: "calc(1.5rem + env(safe-area-inset-right))",
        }}
        className={`fixed w-14 h-14 rounded-full bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg shadow-primary/30 hover:shadow-primary/50 ring-2 ring-primary/40 transition-all duration-300 hover:scale-110 z-[60] ${showChat ? "hidden" : ""}`}
        onClick={() => setShowChat(true)}
      >
        <MessageCircle className="w-6 h-6" />
      </Button>
    </div>
  );
}
