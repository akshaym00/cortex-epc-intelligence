import { useState } from "react";

export default function useProject() {
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

  return {
    projectData,
    setProjectData,
  };
}
