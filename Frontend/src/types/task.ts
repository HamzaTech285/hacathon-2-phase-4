// Types for Task objects

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string;
  user_id: number;
  created_at: string;
  updated_at: string;
  priority?: 'low' | 'medium' | 'high';
  category_id?: string;
  is_recurring?: boolean;
  recurring_frequency?: 'daily' | 'weekly' | 'monthly';
  reminder_enabled?: boolean;
  completed_at?: string;
  due_time?: string;
}