import { useApp } from "../context/AppContext";
import { useState } from "react";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import UploadPanel from "../components/upload/UploadPanel";
import DashboardCard from "../components/common/DashboardCard";
import ExecutiveSummary from "../components/common/ExecutiveSummary";
import AIInsight from "../components/common/AIInsight";
import ProjectControlsBoard from "../components/common/ProjectControlsBoard";
import KnowledgeGraph from "../components/graph/KnowledgeGraph";
import CompliancePanel from "../components/compliance/CompliancePanel";

function ControlsDashboard() {
  const { projectData, updateProjectData } = useApp();
  const [selectedEntityId, setSelectedEntityId] = useState(null);

  const handleEntitySelection = (entityId) => {
    setSelectedEntityId(entityId);
  };

  return (
    <div className="app">
      <Sidebar />
      <main className="main">
        <Header />
        <UploadPanel setProjectData={updateProjectData} />

        <ExecutiveSummary projectData={projectData} />
        <AIInsight projectData={projectData} />
        <ProjectControlsBoard projectData={projectData} />

        <div className="workspace-heading">
          <div><span>PROJECT INTELLIGENCE</span><h2>Project Intelligence</h2></div>
          <p>Model updates appear as source documents are analyzed.</p>
        </div>

        <section className="dashboard-grid">
          <CompliancePanel id="compliance" findings={projectData.compliance_findings} />

          <DashboardCard
            id="entities"
            title="Project Entities"
            items={projectData.entities}
            onEntityClick={handleEntitySelection}
          />

          <DashboardCard
            id="relationships"
            title="Dependency Network"
            items={projectData.relationships}
            onEntityClick={handleEntitySelection}
          />

          <DashboardCard
            id="events"
            title="Project Events"
            items={projectData.events}
          />

          <DashboardCard
            id="impact"
            title="Impact Analysis"
            items={projectData.impacts}
          />

          <DashboardCard
            id="recommendations"
            title="Action Register"
            items={projectData.recommendations}
          />

          <KnowledgeGraph
            id="knowledge-graph"
            entities={projectData.entities}
            relationships={projectData.relationships}
            impacts={projectData.impacts}
            selectedEntityId={selectedEntityId}
            onEntitySelect={handleEntitySelection}
          />
        </section>
      </main>
    </div>
  );
}

export default ControlsDashboard;
