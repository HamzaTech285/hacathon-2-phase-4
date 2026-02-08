import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Backend URL

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the token in all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, remove it
      localStorage.removeItem('access_token');
    }
    return Promise.reject(error);
  }
);

export interface UserCredentials {
  email: string;
  password: string;
}

export interface UserRegistration {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface RegistrationResponse {
  access_token: string;
  token_type: string;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  is_completed: boolean;
  due_date?: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  is_completed?: boolean;
  due_date?: string;
  user_id: number;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
  due_date?: string;
}

export const authService = {
  async login(credentials: UserCredentials): Promise<LoginResponse> {
    const response = await api.post('/login', credentials);
    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    return response.data;
  },

  async register(userData: UserRegistration): Promise<RegistrationResponse> {
    const response = await api.post('/api/auth/signup', userData);
    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    return response.data;
  },

  logout(): void {
    localStorage.removeItem('access_token');
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  },

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }
};

export const taskService = {
  async getAllTasks(completed?: boolean): Promise<Task[]> {
    let url = '/api/tasks/';
    if (completed !== undefined) {
      url += `?completed=${completed}`;
    }
    const response = await api.get(url);
    return response.data;
  },

  async createTask(taskData: TaskCreate): Promise<Task> {
    const response = await api.post('/api/tasks/', taskData);
    return response.data;
  },

  async updateTask(taskId: number, taskData: TaskUpdate): Promise<Task> {
    const response = await api.put(`/api/tasks/${taskId}`, taskData);
    return response.data;
  },

  async deleteTask(taskId: number): Promise<void> {
    await api.delete(`/api/tasks/${taskId}`);
  },

  async getTaskById(taskId: number): Promise<Task> {
    const response = await api.get(`/api/tasks/${taskId}`);
    return response.data;
  }
};

export interface ChatRequest {
  message: string;
  conversation_id?: number;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: any[];
}

export const chatService = {
  async sendMessage(chatData: ChatRequest): Promise<ChatResponse> {
    const response = await api.post('/api/chat', chatData);
    return response.data;
  }
};

export { api };