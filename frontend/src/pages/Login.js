import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { 
  Stethoscope, 
  Eye, 
  EyeOff, 
  AlertCircle, 
  Shield, 
  Users, 
  Lock,
  Mail,
  Loader,
  CheckCircle
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated, isLoading, error, clearError, loginAttempts } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [showDemoCredentials, setShowDemoCredentials] = useState(false);

  const { register, handleSubmit, formState: { errors }, setValue } = useForm();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      const from = location.state?.from?.pathname || '/';
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  // Clear errors when component mounts
  useEffect(() => {
    clearError();
  }, [clearError]);

  const onSubmit = async (data) => {
    const result = await login(data.email, data.password);
    
    if (result.success) {
      toast.success(`Welcome back, ${result.user.name}!`);
      const from = location.state?.from?.pathname || '/';
      navigate(from, { replace: true });
    } else {
      toast.error(result.error);
    }
  };

  const fillDemoCredentials = (role) => {
    const credentials = {
      doctor: { email: 'dr.smith@hospital.com', password: 'MedSecure2024!' },
      nurse: { email: 'nurse.davis@hospital.com', password: 'NurseSecure!' },
      tech: { email: 'tech.wilson@hospital.com', password: 'TechAccess!' },
      admin: { email: 'admin@hospital.com', password: 'AdminSecure2024!' }
    };

    const cred = credentials[role];
    setValue('email', cred.email);
    setValue('password', cred.password);
    setShowDemoCredentials(false);
  };

  const demoRoles = [
    {
      id: 'doctor',
      name: 'Dr. Sarah Smith',
      role: 'Oncologist',
      icon: Stethoscope,
      color: 'bg-primary-500'
    },
    {
      id: 'nurse',
      name: 'Jennifer Davis, RN',
      role: 'Oncology Nurse',
      icon: Users,
      color: 'bg-primary-400'
    },
    {
      id: 'tech',
      name: 'Lisa Wilson, MT',
      role: 'Medical Technologist',
      icon: Shield,
      color: 'bg-primary-600'
    },
    {
      id: 'admin',
      name: 'System Administrator',
      role: 'IT Administrator',
      icon: Lock,
      color: 'bg-primary-700'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-primary-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex items-center justify-center space-x-3 mb-6">
            <div className="flex items-center justify-center w-16 h-16 bg-primary-600 rounded-2xl">
              <Stethoscope className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Breast Cancer AI
              </h1>
              <p className="text-sm text-gray-600">
                Hospital Staff Portal
              </p>
            </div>
          </div>
          
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Secure Access for Healthcare Professionals
          </h2>
          <p className="text-gray-600">
            Please sign in with your hospital credentials
          </p>
        </div>

        {/* Security Notice */}
        <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <Shield className="w-5 h-5 text-primary-600 mt-0.5" />
            <div>
              <h3 className="text-sm font-medium text-primary-800">
                HIPAA Compliant System
              </h3>
              <p className="text-sm text-primary-700 mt-1">
                This system is designed for authorized healthcare professionals only. 
                All access is logged and monitored for security compliance.
              </p>
            </div>
          </div>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Email Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Hospital Email Address
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('email', {
                    required: 'Email is required',
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: 'Invalid email address'
                    }
                  })}
                  type="email"
                  className="input-field pl-10"
                  placeholder="your.name@hospital.com"
                />
              </div>
              {errors.email && (
                <p className="text-red-600 text-sm mt-1">{errors.email.message}</p>
              )}
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('password', {
                    required: 'Password is required',
                    minLength: {
                      value: 8,
                      message: 'Password must be at least 8 characters'
                    }
                  })}
                  type={showPassword ? 'text' : 'password'}
                  className="input-field pl-10 pr-10"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="text-red-600 text-sm mt-1">{errors.password.message}</p>
              )}
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="w-5 h-5 text-red-600" />
                  <p className="text-red-800 text-sm">{error}</p>
                </div>
                {loginAttempts >= 2 && (
                  <p className="text-red-700 text-xs mt-2">
                    Warning: {loginAttempts} failed attempts. Account will be temporarily locked after 3 attempts.
                  </p>
                )}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full btn-primary flex items-center justify-center space-x-2 disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <CheckCircle className="w-5 h-5" />
                  <span>Sign In Securely</span>
                </>
              )}
            </button>
          </form>

          {/* Demo Credentials */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={() => setShowDemoCredentials(!showDemoCredentials)}
              className="w-full text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              {showDemoCredentials ? 'Hide' : 'Show'} Demo Credentials
            </button>

            {showDemoCredentials && (
              <div className="mt-4 space-y-3">
                <p className="text-xs text-gray-600 mb-3">
                  For demonstration purposes only. Click to auto-fill credentials:
                </p>
                
                <div className="grid grid-cols-1 gap-2">
                  {demoRoles.map((role) => (
                    <button
                      key={role.id}
                      type="button"
                      onClick={() => fillDemoCredentials(role.id)}
                      className="flex items-center space-x-3 p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors text-left"
                    >
                      <div className={`${role.color} p-2 rounded-lg`}>
                        <role.icon className="w-4 h-4 text-white" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {role.name}
                        </div>
                        <div className="text-xs text-gray-600">
                          {role.role}
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center">
          <p className="text-xs text-gray-500">
            Protected by enterprise-grade security. All sessions are encrypted and monitored.
          </p>
          <p className="text-xs text-gray-500 mt-1">
            For technical support, contact IT Help Desk: ext. 4357
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;