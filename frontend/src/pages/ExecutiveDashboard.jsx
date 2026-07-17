import { useApp } from "../context/AppContext";
import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import UploadPanel from "../components/upload/UploadPanel";
import ExecutiveSignal from "../components/executive/ExecutiveSignal";
import DecisionPack from "../components/executive/DecisionPack";
import CriticalPathCard from "../components/executive/CriticalPathCard";
import RiskSummary from "../components/executive/RiskSummary";

function ExecutiveDashboard() {
  const { projectData, updateProjectData } = useApp();

  return (
    <div className="app">
      <Sidebar />
      <main className="main">
        <Header />
        <UploadPanel setProjectData={updateProjectData} />
        
        {projectData.entities?.length > 0 ? (
          <>
            <ExecutiveSignal projectData={projectData} />
            <DecisionPack projectData={projectData} />
            <CriticalPathCard projectData={projectData} />
            <RiskSummary projectData={projectData} />
          </>
        ) : (
          <section className="controls-board controls-board-empty">
            <div className="controls-board-heading">
              <span>📊 EXECUTIVE COMMAND CENTER</span>
              <h2>Waiting for project intelligence</h2>
              <p>Upload a schedule risk, RFI log, or vendor submittal to generate executive insights.</p>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default ExecutiveDashboard;
