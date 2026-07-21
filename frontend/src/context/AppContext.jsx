import { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [projectData, setProjectData] = useState({
    entities: [],
    relationships: [],
    events: [],
    impacts: [],
    recommendations: [],
    compliance_findings: [],
    controls_brief: null,
    verification: null,
  });

  const [currentWorkspace, setCurrentWorkspace] = useState('executive');
  const [activeSection, setActiveSection] = useState('command-center');

  const updateProjectData = (newData) => {
    setProjectData((prev) => ({
      ...prev,
      ...(newData || {}),
    }));
  };

  const value = {
    projectData,
    setProjectData,
    updateProjectData,
    currentWorkspace,
    setCurrentWorkspace,
    activeSection,
    setActiveSection,
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
}
