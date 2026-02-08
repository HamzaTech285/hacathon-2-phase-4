/** Signup Page Component */

import React from 'react';
import SignupForm from '../components/auth/SignupForm';
import { useNavigate } from 'react-router-dom';

const SignupPage: React.FC = () => {
  const navigate = useNavigate();

  const handleSignup = () => {
    // Optionally handle post-signup actions
    console.log('User signed up successfully');
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
          Create a new account
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Or{' '}
          <a href="/login" className="font-medium text-blue-600 hover:text-blue-500">
            sign in to your existing account
          </a>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <SignupForm onSignup={handleSignup} />
        </div>
      </div>
    </div>
  );
};

export default SignupPage;