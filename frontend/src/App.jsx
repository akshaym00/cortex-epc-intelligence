import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AppProvider } from "./context/AppContext";
import ExecutiveDashboard from "./pages/ExecutiveDashboard";
import ControlsDashboard from "./pages/ControlsDashboard";

function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <Routes>
          <Route path="/executive" element={<ExecutiveDashboard />} />
          <Route path="/controls" element={<ControlsDashboard />} />
          <Route path="/" element={<Navigate to="/executive" replace />} />
        </Routes>
      </AppProvider>
    </BrowserRouter>
  );
}

export default App;