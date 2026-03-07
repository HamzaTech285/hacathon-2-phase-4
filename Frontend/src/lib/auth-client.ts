/**
 * Better Auth Client Configuration
 * 
 * This module provides authentication utilities compatible with Better Auth
 * while maintaining compatibility with the FastAPI backend JWT system.
 */

import { jwtDecode } from 'jwt-decode';

interface JWTPayload {
  sub: string;
  user_id: number;
  email: string;
  role: string;
  exp: number;
}

interface AuthTokens {
  access_token: string;
  token_type: string;
}

interface User {
  id: number;
  email: string;
  role: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Store authentication tokens
 */
export const setAuthTokens = (tokens: AuthTokens): void => {
  localStorage.setItem('access_token', tokens.access_token);
  localStorage.setItem('token_type', tokens.token_type);
};

/**
 * Get stored access token
 */
export const getAccessToken = (): string | null => {
  return localStorage.getItem('access_token');
};

/**
 * Remove authentication tokens
 */
export const removeAuthTokens = (): void => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('token_type');
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  const token = getAccessToken();
  if (!token) return false;

  try {
    const decoded = jwtDecode<JWTPayload>(token);
    const now = Date.now() / 1000;
    
    // Check if token is expired
    if (decoded.exp < now) {
      removeAuthTokens();
      return false;
    }
    
    return true;
  } catch (error) {
    removeAuthTokens();
    return false;
  }
};

/**
 * Get current user from token
 */
export const getCurrentUser = (): User | null => {
  const token = getAccessToken();
  if (!token) return null;

  try {
    const decoded = jwtDecode<JWTPayload>(token);
    return {
      id: decoded.user_id,
      email: decoded.email,
      role: decoded.role,
    };
  } catch (error) {
    return null;
  }
};

/**
 * Get user ID from token
 */
export const getUserId = (): number | null => {
  const user = getCurrentUser();
  return user?.id || null;
};

/**
 * Sign up with email and password
 */
export const signup = async (email: string, password: string): Promise<AuthTokens> => {
  const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Signup failed');
  }

  const data = await response.json();
  setAuthTokens(data);
  return data;
};

/**
 * Login with email and password
 */
export const login = async (email: string, password: string): Promise<AuthTokens> => {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  const data = await response.json();
  setAuthTokens(data);
  return data;
};

/**
 * Logout user
 */
export const logout = (): void => {
  removeAuthTokens();
  window.location.href = '/auth';
};

/**
 * Get authorization header for API requests
 */
export const getAuthHeader = (): Record<string, string> => {
  const token = getAccessToken();
  if (!token) {
    return {};
  }
  return {
    'Authorization': `Bearer ${token}`,
  };
};

/**
 * Token refresh logic (optional - implement if needed)
 * Currently tokens are not refreshed automatically
 */
export const refreshToken = async (): Promise<AuthTokens | null> => {
  // Implement token refresh if backend supports it
  // For now, users need to re-login when token expires
  return null;
};
