/** Task Item Component to display individual task */

import React, { useState } from 'react';
import { taskService, Task } from '../../services/api';

interface TaskItemProps {
  task: Task;
  onTaskUpdated: (updatedTask: Task) => void;
  onTaskDeleted: (taskId: number) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskUpdated, onTaskDeleted }) => {
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [isDeleting, setIsDeleting] = useState<boolean>(false);
  const [editForm, setEditForm] = useState({
    title: task.title,
    description: task.description || '',
    is_completed: task.completed,
    due_date: task.due_date || ''
  });

  const handleToggleComplete = async () => {
    try {
      const updatedTask = await taskService.updateTask(task.id, {
        is_completed: !task.completed
      });

      // Convert to our Task format
      const convertedTask: Task = {
        ...task,
        completed: updatedTask.is_completed,
        updated_at: updatedTask.updated_at
      };

      onTaskUpdated(convertedTask);
    } catch (err: any) {
      alert(err.message || 'An error occurred while updating the task');
    }
  };

  const handleEditChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setEditForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSaveEdit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const updatedTask = await taskService.updateTask(task.id, {
        title: editForm.title,
        description: editForm.description || undefined,
        is_completed: editForm.is_completed,
        due_date: editForm.due_date || undefined
      });

      // Convert to our Task format
      const convertedTask: Task = {
        ...task,
        title: updatedTask.title,
        description: updatedTask.description,
        completed: updatedTask.is_completed,
        due_date: updatedTask.due_date || undefined,
        updated_at: updatedTask.updated_at
      };

      onTaskUpdated(convertedTask);
      setIsEditing(false);
    } catch (err: any) {
      alert(err.message || 'An error occurred while saving the task');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      setIsDeleting(true);
      await taskService.deleteTask(task.id);
      onTaskDeleted(task.id);
    } catch (err: any) {
      alert(err.message || 'An error occurred while deleting the task');
    } finally {
      setIsDeleting(false);
    }
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  return (
    <div className={`border rounded-lg p-4 shadow-sm transition-all duration-200 ${
      task.is_completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
    }`}>
      {isEditing ? (
        <form onSubmit={handleSaveEdit} className="space-y-3">
          <div>
            <input
              type="text"
              name="title"
              value={editForm.title}
              onChange={handleEditChange}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <textarea
              name="description"
              value={editForm.description}
              onChange={handleEditChange}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="Description (optional)"
            />
          </div>

          <div className="flex items-center space-x-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                name="is_completed"
                checked={editForm.is_completed}
                onChange={(e) => setEditForm(prev => ({ ...prev, is_completed: e.target.checked }))}
                className="mr-2"
              />
              Completed
            </label>

            <input
              type="date"
              name="due_date"
              value={editForm.due_date}
              onChange={handleEditChange}
              className="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex space-x-2">
            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Save
            </button>
            <button
              type="button"
              onClick={() => setIsEditing(false)}
              className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <div>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.is_completed}
              onChange={handleToggleComplete}
              className="mt-1 mr-3 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
            />
            <div className="flex-1">
              <h3 className={`text-lg font-medium ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h3>

              {task.description && (
                <p className={`mt-1 text-gray-600 ${task.is_completed ? 'line-through' : ''}`}>
                  {task.description}
                </p>
              )}

              <div className="mt-2 flex flex-wrap gap-2 text-sm">
                {task.due_date && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                    Due: {formatDate(task.due_date)}
                  </span>
                )}

                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  task.is_completed ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                }`}>
                  {task.is_completed ? 'Completed' : 'Pending'}
                </span>
              </div>
            </div>

            <div className="flex space-x-2 ml-2">
              <button
                onClick={() => setIsEditing(true)}
                className="text-blue-600 hover:text-blue-900 p-1 rounded-full hover:bg-blue-100"
                aria-label="Edit task"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>

              <button
                onClick={handleDelete}
                disabled={isDeleting}
                className={`${isDeleting ? 'text-gray-400' : 'text-red-600 hover:text-red-900'} p-1 rounded-full hover:bg-red-100`}
                aria-label="Delete task"
              >
                {isDeleting ? (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 animate-spin" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;