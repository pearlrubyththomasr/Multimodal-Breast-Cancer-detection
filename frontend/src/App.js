import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import PatientAnalysis from './pages/PatientAnalysis';
import Results from './pages/Results';
import Analytics from './pages/Analytics';
import PatientManagement from './pages/PatientManagement';
import About from './pages/About';
import { AnalysisProvider } from './context/AnalysisContext';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <AnalysisProvider>
        <Router>
          <Routes>
            {/* Public Route */}
            <Route path="/login" element={<Login />} />
            
            {/* Protected Routes */}
            <Route path="/*" element={
              <ProtectedRoute>
                <div className="min-h-screen bg-medical-50">
                  <Navbar />
                  <main className="container mx-auto px-4 py-8">
                    <Routes>
                      <Route path="/" element={<Dashboard />} />
                      <Route path="/analysis" element={
                        <ProtectedRoute requiredPermission="analysis">
                          <PatientAnalysis />
                        </ProtectedRoute>
                      } />
                      <Route path="/results/:patientId" element={
                        <ProtectedRoute requiredPermission="results">
                          <Results />
                        </ProtectedRoute>
                      } />
                      <Route path="/analytics" element={
                        <ProtectedRoute requiredPermission="analytics">
                          <Analytics />
                        </ProtectedRoute>
                      } />
                      <Route path="/patients" element={
                        <ProtectedRoute requiredPermission="patients">
                          <PatientManagement />
                        </ProtectedRoute>
                      } />
                      <Route path="/about" element={<About />} />
                    </Routes>
                  </main>
                </div>
              </ProtectedRoute>
            } />
          </Routes>
          
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
        </Router>
      </AnalysisProvider>
    </AuthProvider>
  );
}

export default App;