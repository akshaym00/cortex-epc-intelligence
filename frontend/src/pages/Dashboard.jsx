import useProject from "../hooks/useProject";

import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import UploadPanel from "../components/upload/UploadPanel";
import DashboardCard from "../components/common/DashboardCard";
import ExecutiveSummary from "../components/common/ExecutiveSummary";
import AIInsight from "../components/common/AIInsight";
import ProjectControlsBoard from "../components/common/ProjectControlsBoard";
import KnowledgeGraph from "../components/graph/KnowledgeGraph";
import CompliancePanel from "../components/compliance/CompliancePanel";

function Dashboard() {

  const {
    projectData,
    setProjectData,
  } = useProject();

  return (
    <div className="app">

      <Sidebar />

      <main className="main">

        <Header />

        <UploadPanel
          setProjectData={setProjectData}
        />

        <ExecutiveSummary projectData={projectData} />

        <AIInsight projectData={projectData} />

        <ProjectControlsBoard projectData={projectData} />

        <div className="workspace-heading">
          <div><span>PROJECT INTELLIGENCE</span><h2>Project Intelligence</h2></div>
          <p>Model updates appear as source documents are analyzed.</p>
        </div>

        <section className="dashboard-grid">

          <CompliancePanel findings={projectData.compliance_findings} />

          <DashboardCard
            title="Entities"
            items={projectData.entities}
          />

          <DashboardCard
            title="Relationships"
            items={projectData.relationships}
          />

          <DashboardCard
            title="Events"
            items={projectData.events}
          />

          <DashboardCard
            title="Impact Analysis"
            items={projectData.impacts}
          />

          <DashboardCard
            title="Recommendations"
            items={projectData.recommendations}
          />

          <KnowledgeGraph
            entities={projectData.entities}
            relationships={projectData.relationships}
            impacts={projectData.impacts}
          />

        </section>

      </main>

    </div>
  );
}

export default Dashboard;
