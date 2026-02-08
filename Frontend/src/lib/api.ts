/** API utility functions for interacting with the backend */

import { Task } from '../types/task';
import { maybeRefreshToken, getToken } from '../utils/auth';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

/**
 * Get the authorization header with the stored token
 */
const getAuthHeaders = () => {
  const token = getToken();
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
};

/**
 * Make an authenticated API request with token refresh capability
 */
const makeAuthenticatedRequest = async (
  url: string,
  options: RequestInit = {}
): Promise<Response> => {
  // First, try to refresh the token if needed
  await maybeRefreshToken();

  // Add auth headers to the request
  const authHeaders = getAuthHeaders();
  const requestOptions = {
    ...options,
    headers: {
      ...options.headers,
      ...authHeaders,
    },
  };

  let response = await fetch(url, requestOptions);

  // If the response is 401 (Unauthorized), try to refresh the token and retry
  if (response.status === 401) {
    // Attempt to refresh the token
    const refreshed = await maybeRefreshToken();

    if (refreshed) {
      // Retry the request with the new token
      const newAuthHeaders = getAuthHeaders();
      const retryOptions = {
        ...options,
        headers: {
          ...options.headers,
          ...newAuthHeaders,
        },
      };

      response = await fetch(url, retryOptions);
    }
  }

  return response;
};

/**
 * User Authentication API functions
 */

export const authAPI = {
  /**
   * Register a new user
   */
  signup: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Registration failed');
    }

    return data;
  },

  /**
   * Login a user
   */
  login: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Login failed');
    }

    return data;
  },
};

/**
 * Task API functions
 */

export const taskAPI = {
  /**
   * Get all tasks for the authenticated user
   */
  getTasks: async (completed?: boolean): Promise<Task[]> => {
    let url = `${API_BASE_URL}/tasks`;
    if (completed !== undefined) {
      url += `?completed=${completed}`;
    }

    const response = await makeAuthenticatedRequest(url);

    if (!response.ok) {
      if (response.status === 401) {
        // Token is invalid or expired after refresh attempts
        // Redirect to auth
        window.location.href = '/auth';
        throw new Error('Session expired. Please log in again.');
      }

      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch tasks');
    }

    return response.json();
  },

  /**
   * Create a new task
   */
  createTask: async (taskData: Partial<Task>): Promise<Task> => {
    const response = await makeAuthenticatedRequest(`${API_BASE_URL}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token is invalid or expired after refresh attempts
        // Redirect to auth
        window.location.href = '/auth';
        throw new Error('Session expired. Please log in again.');
      }

      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to create task');
    }

    return response.json();
  },

  /**
   * Get a specific task by ID
   */
  getTaskById: async (taskId: number): Promise<Task> => {
    const response = await makeAuthenticatedRequest(`${API_BASE_URL}/tasks/${taskId}`);

    if (!response.ok) {
      if (response.status === 401) {
        // Token is invalid or expired after refresh attempts
        // Redirect to auth
        window.location.href = '/auth';
        throw new Error('Session expired. Please log in again.');
      }

      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch task');
    }

    return response.json();
  },

  /**
   * Update a task
   */
  updateTask: async (taskId: number, taskData: Partial<Task>): Promise<Task> => {
    const response = await makeAuthenticatedRequest(`${API_BASE_URL}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token is invalid or expired after refresh attempts
        // Redirect to auth
        window.location.href = '/auth';
        throw new Error('Session expired. Please log in again.');
      }

      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to update task');
    }

    return response.json();
  },

  /**
   * Delete a task
   */
  deleteTask: async (taskId: number): Promise<void> => {
    const response = await makeAuthenticatedRequest(`${API_BASE_URL}/tasks/${taskId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token is invalid or expired after refresh attempts
        // Redirect to auth
        window.location.href = '/auth';
        throw new Error('Session expired. Please log in again.');
      }

      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to delete task');
    }
  },
};