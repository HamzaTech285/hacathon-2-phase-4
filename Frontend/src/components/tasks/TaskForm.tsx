/** Task Form Component for creating new tasks */

import React, { useState } from 'react';
import { taskService, Task } from '../../services/api';

interface TaskFormProps {
  onTaskAdded: (newTask: Task) => void;
  onCancel?: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ onTaskAdded, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    due_date: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // For now, using a placeholder user ID - in a real app this would come from auth context
      const userId = 1;

      const newTask = await taskService.createTask({
        title: formData.title,
        description: formData.description || undefined,
        due_date: formData.due_date || undefined,
        user_id: userId
      });

      // Convert to our Task format
      const convertedTask: Task = {
        id: newTask.id,
        title: newTask.title,
        description: newTask.description,
        completed: newTask.is_completed,
        due_date: newTask.due_date || undefined,
        user_id: newTask.user_id,
        created_at: newTask.created_at,
        updated_at: newTask.updated_at,
        priority: "medium", // Default priority
        category_id: undefined,
        is_recurring: false,
        recurring_frequency: undefined,
        reminder_enabled: false,
        completed_at: newTask.is_completed ? newTask.updated_at : undefined,
        due_time: undefined
      };

      onTaskAdded(convertedTask);

      // Reset form
      setFormData({
        title: '',
        description: '',
        due_date: ''
      });
    } catch (err: any) {
      setError(err.message || 'An error occurred while creating the task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Create New Task</h3>

      {error && (
        <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="What needs to be done?"
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Add details..."
          />
        </div>

        <div>
          <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 mb-1">
            Due Date
          </label>
          <input
            type="date"
            id="due_date"
            name="due_date"
            value={formData.due_date}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div className="flex space-x-3 pt-2">
          <button
            type="submit"
            disabled={loading}
            className={`flex-1 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white ${
              loading ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'
            } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
          >
            {loading ? 'Creating...' : 'Create Task'}
          </button>

          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default TaskForm;