import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { apiUtils } from '../services/api';

// Initial state
const initialState = {
  // Backend status
  backendHealth: {
    isHealthy: false,
    isChecking: true,
    lastChecked: null,
    error: null
  },
  
  // Available modalities
  availableModalities: [],
  
  // Current analysis
  currentAnalysis: {
    isLoading: false,
    patientData: null,
    results: null,
    error: null
  },
  
  // Analysis history
  analysisHistory: [],
  
  // UI state
  ui: {
    activeTab: 'patient-info',
    showAdvanced: false
  }
};

// Action types
const ActionTypes = {
  // Backend health
  SET_BACKEND_HEALTH_CHECKING: 'SET_BACKEND_HEALTH_CHECKING',
  SET_BACKEND_HEALTH: 'SET_BACKEND_HEALTH',
  SET_BACKEND_HEALTH_ERROR: 'SET_BACKEND_HEALTH_ERROR',
  
  // Modalities
  SET_AVAILABLE_MODALITIES: 'SET_AVAILABLE_MODALITIES',
  
  // Analysis
  START_ANALYSIS: 'START_ANALYSIS',
  SET_ANALYSIS_RESULTS: 'SET_ANALYSIS_RESULTS',
  SET_ANALYSIS_ERROR: 'SET_ANALYSIS_ERROR',
  CLEAR_ANALYSIS: 'CLEAR_ANALYSIS',
  
  // History
  ADD_TO_HISTORY: 'ADD_TO_HISTORY',
  CLEAR_HISTORY: 'CLEAR_HISTORY',
  
  // UI
  SET_ACTIVE_TAB: 'SET_ACTIVE_TAB',
  TOGGLE_ADVANCED: 'TOGGLE_ADVANCED'
};

// Reducer
function analysisReducer(state, action) {
  switch (action.type) {
    case ActionTypes.SET_BACKEND_HEALTH_CHECKING:
      return {
        ...state,
        backendHealth: {
          ...state.backendHealth,
          isChecking: action.payload
        }
      };
      
    case ActionTypes.SET_BACKEND_HEALTH:
      return {
        ...state,
        backendHealth: {
          isHealthy: action.payload.isHealthy,
          isChecking: false,
          lastChecked: new Date(),
          error: null,
          data: action.payload.data
        }
      };
      
    case ActionTypes.SET_BACKEND_HEALTH_ERROR:
      return {
        ...state,
        backendHealth: {
          isHealthy: false,
          isChecking: false,
          lastChecked: new Date(),
          error: action.payload
        }
      };
      
    case ActionTypes.SET_AVAILABLE_MODALITIES:
      return {
        ...state,
        availableModalities: action.payload
      };
      
    case ActionTypes.START_ANALYSIS:
      return {
        ...state,
        currentAnalysis: {
          isLoading: true,
          patientData: action.payload,
          results: null,
          error: null
        }
      };
      
    case ActionTypes.SET_ANALYSIS_RESULTS:
      return {
        ...state,
        currentAnalysis: {
          isLoading: false,
          patientData: state.currentAnalysis.patientData,
          results: action.payload,
          error: null
        }
      };
      
    case ActionTypes.SET_ANALYSIS_ERROR:
      return {
        ...state,
        currentAnalysis: {
          isLoading: false,
          patientData: state.currentAnalysis.patientData,
          results: null,
          error: action.payload
        }
      };
      
    case ActionTypes.CLEAR_ANALYSIS:
      return {
        ...state,
        currentAnalysis: {
          isLoading: false,
          patientData: null,
          results: null,
          error: null
        }
      };
      
    case ActionTypes.ADD_TO_HISTORY:
      return {
        ...state,
        analysisHistory: [action.payload, ...state.analysisHistory.slice(0, 9)] // Keep last 10
      };
      
    case ActionTypes.CLEAR_HISTORY:
      return {
        ...state,
        analysisHistory: []
      };
      
    case ActionTypes.SET_ACTIVE_TAB:
      return {
        ...state,
        ui: {
          ...state.ui,
          activeTab: action.payload
        }
      };
      
    case ActionTypes.TOGGLE_ADVANCED:
      return {
        ...state,
        ui: {
          ...state.ui,
          showAdvanced: !state.ui.showAdvanced
        }
      };
      
    default:
      return state;
  }
}

// Context
const AnalysisContext = createContext();

// Provider component
export function AnalysisProvider({ children }) {
  const [state, dispatch] = useReducer(analysisReducer, initialState);

  // Check backend health on mount and periodically
  useEffect(() => {
    checkBackendHealth();
    
    // Check every 30 seconds
    const interval = setInterval(checkBackendHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Load available modalities when backend becomes healthy
  useEffect(() => {
    if (state.backendHealth.isHealthy) {
      loadAvailableModalities();
    }
  }, [state.backendHealth.isHealthy]);

  // Actions
  const checkBackendHealth = async () => {
    dispatch({ type: ActionTypes.SET_BACKEND_HEALTH_CHECKING, payload: true });
    
    try {
      const result = await apiUtils.checkBackendHealth();
      dispatch({ type: ActionTypes.SET_BACKEND_HEALTH, payload: result });
    } catch (error) {
      dispatch({ type: ActionTypes.SET_BACKEND_HEALTH_ERROR, payload: error.message });
    }
  };

  const loadAvailableModalities = async () => {
    try {
      const result = await apiUtils.getAvailableModalities();
      if (result.success) {
        dispatch({ type: ActionTypes.SET_AVAILABLE_MODALITIES, payload: result.modalities });
      }
    } catch (error) {
      console.error('Failed to load modalities:', error);
    }
  };

  const performAnalysis = async (patientData) => {
    dispatch({ type: ActionTypes.START_ANALYSIS, payload: patientData });
    
    try {
      const formattedData = apiUtils.formatPatientData(patientData);
      const result = await apiUtils.performComprehensiveAnalysis(formattedData);
      
      if (result.success) {
        dispatch({ type: ActionTypes.SET_ANALYSIS_RESULTS, payload: result.data });
        
        // Add to history
        const historyEntry = {
          id: Date.now(),
          patientId: result.data.patient_id,
          timestamp: new Date(),
          results: result.data,
          patientData: patientData
        };
        dispatch({ type: ActionTypes.ADD_TO_HISTORY, payload: historyEntry });
        
        return { success: true, data: result.data };
      } else {
        dispatch({ type: ActionTypes.SET_ANALYSIS_ERROR, payload: result.error });
        return { success: false, error: result.error };
      }
    } catch (error) {
      const errorMessage = error.message || 'Analysis failed';
      dispatch({ type: ActionTypes.SET_ANALYSIS_ERROR, payload: errorMessage });
      return { success: false, error: errorMessage };
    }
  };

  const clearAnalysis = () => {
    dispatch({ type: ActionTypes.CLEAR_ANALYSIS });
  };

  const setActiveTab = (tab) => {
    dispatch({ type: ActionTypes.SET_ACTIVE_TAB, payload: tab });
  };

  const toggleAdvanced = () => {
    dispatch({ type: ActionTypes.TOGGLE_ADVANCED });
  };

  const clearHistory = () => {
    dispatch({ type: ActionTypes.CLEAR_HISTORY });
  };

  // Context value
  const value = {
    // State
    ...state,
    
    // Actions
    checkBackendHealth,
    loadAvailableModalities,
    performAnalysis,
    clearAnalysis,
    setActiveTab,
    toggleAdvanced,
    clearHistory
  };

  return (
    <AnalysisContext.Provider value={value}>
      {children}
    </AnalysisContext.Provider>
  );
}

// Hook to use the context
export function useAnalysis() {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error('useAnalysis must be used within an AnalysisProvider');
  }
  return context;
}

export default AnalysisContext;