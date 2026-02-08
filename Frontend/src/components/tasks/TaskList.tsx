/** Task List Component to display user's tasks */

import React, { useState, useEffect } from 'react';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';
import { taskService, Task } from '../../services/api';

interface TaskListProps {
  userId: number;
}

const TaskList: React.FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState<boolean>(false);

  // Fetch tasks for the user
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const backendTasks = await taskService.getAllTasks();
      // Convert backend tasks to our Task format
      const convertedTasks: Task[] = backendTasks.map(task => ({
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
      setTasks(convertedTasks);
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleTaskAdded = (newTask: Task) => {
    setTasks([...tasks, newTask]);
    setShowForm(false);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId: number) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error: </strong>
        <span className="block sm:inline">{error}</span>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Your Tasks</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          {showForm ? 'Cancel' : '+ New Task'}
        </button>
      </div>

      {showForm && (
        <div className="mb-6">
          <TaskForm onTaskAdded={handleTaskAdded} />
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">You don't have any tasks yet.</p>
          <p className="text-gray-400 mt-2">Click "New Task" to get started!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onTaskUpdated={handleTaskUpdated}
              onTaskDeleted={handleTaskDeleted}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;