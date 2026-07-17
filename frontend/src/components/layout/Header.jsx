import { useEffect, useState } from "react";

function Header() {
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' }));

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="header">
      <div>
        <span className="header-eyebrow">PROJECT CONTROLS / LIVE INTELLIGENCE</span>
        <h1>Data Centre Delivery Command</h1>
        <p>Dependency intelligence, schedule exposure and technical assurance in one operational view.</p>
      </div>
      <div className="header-context">
        <div><span>AI Model</span><strong>● Live</strong></div>
        <div><span>Last Analysis</span><strong>{currentTime}</strong></div>
        <div><span>Documents</span><strong>42 indexed</strong></div>
        <div><span>Project</span><strong>DC-MAA-01</strong></div>
        <div><span>Phase</span><strong>Construction</strong></div>
        <div className="live-status"><i /> Live model</div>
      </div>
    </header>
  );
}

export default Header;
