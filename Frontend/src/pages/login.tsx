/** Login Page Component */

import React from 'react';
import LoginForm from '../components/auth/LoginForm';
import { useNavigate } from 'react-router-dom';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    // Optionally handle post-login actions
    console.log('User logged in successfully');
  };

  // Check if user is already logged in
  React.useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      // If user is already logged in, redirect to dashboard
      navigate('/dashboard');
    }
  }, [navigate]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to your account
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Or{' '}
          <a href="/signup" className="font-medium text-blue-600 hover:text-blue-500">
            create a new account
          </a>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <LoginForm onLogin={handleLogin} />
        </div>
      </div>
    </div>
  );
};

export default LoginPage;