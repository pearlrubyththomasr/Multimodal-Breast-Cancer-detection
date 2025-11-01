import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Activity, Brain, Stethoscope, Info, Home, LogOut, User, Shield } from 'lucide-react';
import { useAnalysis } from '../context/AnalysisContext';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const location = useLocation();
  const { backendHealth } = useAnalysis();
  const { user, logout, isDoctor, isNurse, isAdmin } = useAuth();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/analysis', label: 'New Analysis', icon: Brain },
    { path: '/about', label: 'About', icon: Info },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="bg-white shadow-sm border-b border-medical-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Title */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
              <Stethoscope className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-medical-900">
                Breast Cancer AI
              </h1>
              <p className="text-sm text-medical-500">
                Multi-Modal Analysis Platform
              </p>
            </div>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors duration-200 ${
                  isActive(path)
                    ? 'bg-primary-50 text-primary-700 font-medium'
                    : 'text-medical-600 hover:text-medical-900 hover:bg-medical-50'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{label}</span>
              </Link>
            ))}
          </div>

          {/* User Info & Status */}
          <div className="flex items-center space-x-6">
            {/* Backend Status */}
            <div className="flex items-center space-x-2">
              <div
                className={`w-3 h-3 rounded-full ${
                  backendHealth.isChecking
                    ? 'bg-yellow-400 animate-pulse'
                    : backendHealth.isHealthy
                    ? 'bg-green-400'
                    : 'bg-red-400'
                }`}
              />
              <span className="text-sm text-medical-600">
                {backendHealth.isChecking
                  ? 'Checking...'
                  : backendHealth.isHealthy
                  ? 'AI System Online'
                  : 'AI System Offline'}
              </span>
            </div>

            {/* User Profile */}
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  isDoctor() ? 'bg-primary-100' : 
                  isNurse() ? 'bg-primary-200' : 
                  isAdmin() ? 'bg-primary-300' : 'bg-primary-50'
                }`}>
                  {isDoctor() ? (
                    <Stethoscope className={`w-4 h-4 ${
                      isDoctor() ? 'text-primary-600' : 
                      isNurse() ? 'text-primary-700' : 
                      isAdmin() ? 'text-primary-800' : 'text-primary-500'
                    }`} />
                  ) : isAdmin() ? (
                    <Shield className="w-4 h-4 text-primary-800" />
                  ) : (
                    <User className="w-4 h-4 text-primary-600" />
                  )}
                </div>
                <div className="hidden md:block">
                  <p className="text-sm font-medium text-medical-900">
                    {user?.name}
                  </p>
                  <p className="text-xs text-medical-500">
                    {user?.role} • {user?.department}
                  </p>
                </div>
              </div>

              {/* Logout Button */}
              <button
                onClick={logout}
                className="p-2 rounded-lg hover:bg-medical-100 transition-colors text-medical-600 hover:text-medical-900"
                title="Sign Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button className="p-2 rounded-lg text-medical-600 hover:bg-medical-50">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden border-t border-medical-200">
          <div className="py-2 space-y-1">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors duration-200 ${
                  isActive(path)
                    ? 'bg-primary-50 text-primary-700 font-medium'
                    : 'text-medical-600 hover:text-medical-900 hover:bg-medical-50'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;