// Utility functions for authentication

import { authService } from '@/services/api';

/**
 * Check if user is authenticated by checking for token in localStorage
 */
export const isAuthenticated = (): boolean => {
  return authService.isAuthenticated();
};

/**
 * Remove authentication token from localStorage
 */
export const removeToken = (): void => {
  authService.logout();
};

/**
 * Get the authentication token
 */
export const getToken = (): string | null => {
  return authService.getToken();
};