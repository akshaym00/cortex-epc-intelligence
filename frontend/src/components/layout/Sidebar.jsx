import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useApp } from "../../context/AppContext";

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const { projectData, setCurrentWorkspace, activeSection, setActiveSection } = useApp();
  const [observedSections, setObservedSections] = useState(new Set());

  const workspaces = [
    { id: "executive", label: "Executive Command Center", path: "/executive", icon: "▦" },
    { id: "controls", label: "Project Controls Workspace", path: "/controls", icon: "⚙" },
  ];

  const controlsNavItems = [
    { id: "entities", label: "Project Entities", icon: "◇" },
    { id: "relationships", label: "Dependency Network", icon: "⌁" },
    { id: "events", label: "Project Events", icon: "⚡" },
    { id: "impact", label: "Impact Analysis", icon: "△" },
    { id: "recommendations", label: "Action Register", icon: "✓" },
    { id: "knowledge-graph", label: "Project Knowledge Graph", icon: "⬡" },
  ];

  const isExecutive = location.pathname === "/executive";
  const isControls = location.pathname === "/controls";

  const handleWorkspaceClick = (workspace) => {
    setCurrentWorkspace(workspace.id);
    navigate(workspace.path);
  };

  const handleSectionClick = (sectionId) => {
    setActiveSection(sectionId);
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  // Intersection Observer for active section highlighting
  useEffect(() => {
    if (!isControls) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const visibleSections = new Set();
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            visibleSections.add(entry.target.id);
          }
        });

        if (visibleSections.size > 0) {
          // Set the first visible section as active
          const firstVisible = Array.from(visibleSections)[0];
          setActiveSection(firstVisible);
        }
      },
      { threshold: 0.3 },
    );

    controlsNavItems.forEach((item) => {
      const element = document.getElementById(item.id);
      if (element) {
        observer.observe(element);
      }
    });

    return () => observer.disconnect();
  }, [isControls, setActiveSection]);

  const stats = {
    entities: projectData.entities?.length || 0,
    relationships: projectData.relationships?.length || 0,
    events: projectData.events?.length || 0,
    confidence: projectData.controls_brief?.confidence || 85,
  };

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">CX</div>
        <div><h2>CORTEX</h2><span>EPC Intelligence</span></div>
      </div>

      <nav>
        {/* Command Center Section */}
        <div className="nav-section">
          <div className="nav-section-label">📊 COMMAND CENTER</div>
          <ul>
            {workspaces.map((workspace) => (
              <li
                key={workspace.id}
                className={
                  (workspace.id === "executive" && isExecutive) ||
                  (workspace.id === "controls" && isControls)
                    ? "active"
                    : ""
                }
                onClick={() => handleWorkspaceClick(workspace)}
                role="button"
                tabIndex="0"
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    handleWorkspaceClick(workspace);
                  }
                }}
              >
                <span>{workspace.icon}</span>
                {workspace.label}
              </li>
            ))}
          </ul>
        </div>

        {/* Project Intelligence Section - Show only in Controls Workspace */}
        {isControls && (
          <div className="nav-section">
            <div className="nav-section-label">🧠 PROJECT INTELLIGENCE</div>
            <ul>
              {controlsNavItems.map((item) => (
                <li
                  key={item.id}
                  className={activeSection === item.id ? "active" : ""}
                  onClick={() => handleSectionClick(item.id)}
                  role="button"
                  tabIndex="0"
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      handleSectionClick(item.id);
                    }
                  }}
                >
                  <span>{item.icon}</span>
                  {item.label}
                </li>
              ))}
            </ul>
          </div>
        )}
      </nav>

      <div className="sidebar-footer">
        {projectData.entities?.length > 0 ? (
          <div className="project-summary">
            <div className="summary-divider">───────────────────</div>
            <div className="summary-section">
              <span className="summary-label">STATUS</span>
              <strong className="status-live">🟢 Live</strong>
            </div>
            <div className="summary-section">
              <span className="summary-label">Entities</span>
              <strong>{stats.entities}</strong>
            </div>
            <div className="summary-section">
              <span className="summary-label">Relationships</span>
              <strong>{stats.relationships}</strong>
            </div>
            <div className="summary-section">
              <span className="summary-label">Events</span>
              <strong>{stats.events}</strong>
            </div>
            <div className="summary-section">
              <span className="summary-label">AI Confidence</span>
              <strong>{stats.confidence}%</strong>
            </div>
            <div className="summary-divider">───────────────────</div>
          </div>
        ) : null}
        <div className="model-health"><i /><span><strong>Model online</strong><small>All systems operational</small></span></div>
      </div>
    </aside>
  );
}

export default Sidebar;
