import { Routes, Route } from "react-router-dom";

import Chat from "../pages/chat/chat";
import Auth from "../pages/chat/Auth/Auth";
import HealthPage from "../pages/Health/HealthPage";

function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Auth />} />
      <Route path="/chat" element={<Chat />} />
      <Route path="/health" element={<HealthPage />} />
    </Routes>
  );
}

export default AppRouter;
