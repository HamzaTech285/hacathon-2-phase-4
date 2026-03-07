// Utility functions for authentication
// Compatible with Better Auth JWT system

import {
  isAuthenticated as checkAuth,
  removeAuthTokens,
  getAccessToken,
  getCurrentUser,
  getUserId,
} from '@/lib/auth-client';

/**
 * Check if user is authenticated by validating JWT token
 */
export const isAuthenticated = (): boolean => {
  return checkAuth();
};

/**
 * Remove authentication token from localStorage
 */
export const removeToken = (): void => {
  removeAuthTokens();
};

/**
 * Get the authentication token
 */
export const getToken = (): string | null => {
  return getAccessToken();
};

/**
 * Get current user information from JWT token
 */
export const getCurrentUserFromToken = () => {
  return getCurrentUser();
};

/**
 * Get user ID from JWT token
 */
export const getUserIdFromToken = (): number | null => {
  return getUserId();
};