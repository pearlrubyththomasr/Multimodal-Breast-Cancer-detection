import React, { createContext, useContext, useReducer, useEffect } from 'react';

// Initial state
const initialState = {
  isAuthenticated: false,
  user: null,
  isLoading: true,
  error: null,
  loginAttempts: 0,
  lastLoginAttempt: null
};

// Action types
const ActionTypes = {
  LOGIN_START: 'LOGIN_START',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_FAILURE: 'LOGIN_FAILURE',
  LOGOUT: 'LOGOUT',
  CLEAR_ERROR: 'CLEAR_ERROR',
  SET_LOADING: 'SET_LOADING'
};

// Reducer
function authReducer(state, action) {
  switch (action.type) {
    case ActionTypes.LOGIN_START:
      return {
        ...state,
        isLoading: true,
        error: null
      };

    case ActionTypes.LOGIN_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload,
        isLoading: false,
        error: null,
        loginAttempts: 0
      };

    case ActionTypes.LOGIN_FAILURE:
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        isLoading: false,
        error: action.payload,
        loginAttempts: state.loginAttempts + 1,
        lastLoginAttempt: new Date()
      };

    case ActionTypes.LOGOUT:
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        error: null
      };

    case ActionTypes.CLEAR_ERROR:
      return {
        ...state,
        error: null
      };

    case ActionTypes.SET_LOADING:
      return {
        ...state,
        isLoading: action.payload
      };

    default:
      return state;
  }
}

// Mock hospital staff database
const HOSPITAL_STAFF = {
  // Doctors
  'dr.smith@hospital.com': {
    password: 'MedSecure2024!',
    name: 'Dr. Sarah Smith',
    role: 'Oncologist',
    department: 'Oncology',
    license: 'MD12345',
    permissions: ['analysis', 'results', 'export', 'analytics', 'patients']
  },
  'dr.johnson@hospital.com': {
    password: 'DocPass123!',
    name: 'Dr. Michael Johnson',
    role: 'Radiologist',
    department: 'Radiology',
    license: 'MD67890',
    permissions: ['analysis', 'results', 'imaging', 'analytics', 'patients']
  },
  'dr.williams@hospital.com': {
    password: 'Clinical2024!',
    name: 'Dr. Emily Williams',
    role: 'Pathologist',
    department: 'Pathology',
    license: 'MD54321',
    permissions: ['analysis', 'results', 'genomics', 'analytics', 'patients']
  },

  // Nurses
  'nurse.davis@hospital.com': {
    password: 'NurseSecure!',
    name: 'Jennifer Davis, RN',
    role: 'Oncology Nurse',
    department: 'Oncology',
    license: 'RN98765',
    permissions: ['analysis', 'results', 'analytics']
  },
  'nurse.brown@hospital.com': {
    password: 'CareTeam123!',
    name: 'Robert Brown, RN',
    role: 'Clinical Nurse',
    department: 'General Medicine',
    license: 'RN13579',
    permissions: ['analysis', 'analytics']
  },

  // Medical Technologists
  'tech.wilson@hospital.com': {
    password: 'TechAccess!',
    name: 'Lisa Wilson, MT',
    role: 'Medical Technologist',
    department: 'Laboratory',
    license: 'MT24680',
    permissions: ['analysis', 'results', 'analytics']
  },

  // Administrators
  'admin@hospital.com': {
    password: 'AdminSecure2024!',
    name: 'Hospital Administrator',
    role: 'System Administrator',
    department: 'IT/Administration',
    license: 'ADMIN001',
    permissions: ['analysis', 'results', 'export', 'admin', 'analytics', 'patients']
  }
};

// Context
const AuthContext = createContext();

// Provider component
export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check for existing session on mount
  useEffect(() => {
    checkExistingSession();
  }, []);

  // Auto-logout after inactivity
  useEffect(() => {
    if (state.isAuthenticated) {
      const timeout = setTimeout(() => {
        logout();
      }, 30 * 60 * 1000); // 30 minutes

      return () => clearTimeout(timeout);
    }
  }, [state.isAuthenticated]);

  const checkExistingSession = () => {
    try {
      const savedUser = localStorage.getItem('hospital_auth_user');
      const sessionExpiry = localStorage.getItem('hospital_auth_expiry');

      if (savedUser && sessionExpiry) {
        const now = new Date().getTime();
        const expiry = parseInt(sessionExpiry);

        if (now < expiry) {
          const user = JSON.parse(savedUser);
          dispatch({ type: ActionTypes.LOGIN_SUCCESS, payload: user });
        } else {
          // Session expired
          localStorage.removeItem('hospital_auth_user');
          localStorage.removeItem('hospital_auth_expiry');
        }
      }
    } catch (error) {
      console.error('Session check error:', error);
    } finally {
      dispatch({ type: ActionTypes.SET_LOADING, payload: false });
    }
  };

  const login = async (email, password) => {
    dispatch({ type: ActionTypes.LOGIN_START });

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    try {
      // Validate credentials
      const normalizedEmail = email.toLowerCase().trim();
      const staff = HOSPITAL_STAFF[normalizedEmail];

      if (!staff || staff.password !== password) {
        throw new Error('Invalid email or password');
      }

      // Check for too many failed attempts
      if (state.loginAttempts >= 3) {
        const timeSinceLastAttempt = new Date() - state.lastLoginAttempt;
        if (timeSinceLastAttempt < 15 * 60 * 1000) { // 15 minutes
          throw new Error('Too many failed attempts. Please try again in 15 minutes.');
        }
      }

      // Create user session
      const user = {
        email: normalizedEmail,
        name: staff.name,
        role: staff.role,
        department: staff.department,
        license: staff.license,
        permissions: staff.permissions,
        loginTime: new Date().toISOString()
      };

      // Save session
      const expiry = new Date().getTime() + (8 * 60 * 60 * 1000); // 8 hours
      localStorage.setItem('hospital_auth_user', JSON.stringify(user));
      localStorage.setItem('hospital_auth_expiry', expiry.toString());

      dispatch({ type: ActionTypes.LOGIN_SUCCESS, payload: user });

      return { success: true, user };
    } catch (error) {
      dispatch({ type: ActionTypes.LOGIN_FAILURE, payload: error.message });
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    localStorage.removeItem('hospital_auth_user');
    localStorage.removeItem('hospital_auth_expiry');
    dispatch({ type: ActionTypes.LOGOUT });
  };

  const clearError = () => {
    dispatch({ type: ActionTypes.CLEAR_ERROR });
  };

  const hasPermission = (permission) => {
    return state.user?.permissions?.includes(permission) || false;
  };

  const isDoctor = () => {
    return state.user?.role?.toLowerCase().includes('dr.') ||
      state.user?.license?.startsWith('MD');
  };

  const isNurse = () => {
    return state.user?.role?.toLowerCase().includes('nurse') ||
      state.user?.license?.startsWith('RN');
  };

  const isAdmin = () => {
    return hasPermission('admin');
  };

  // Context value
  const value = {
    // State
    ...state,

    // Actions
    login,
    logout,
    clearError,

    // Utilities
    hasPermission,
    isDoctor,
    isNurse,
    isAdmin
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook to use the context
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;