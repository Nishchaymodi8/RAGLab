import { Routes, Route } from "react-router-dom";

import Chat from "../pages/chat/chat";
import Auth from "../pages/chat/Auth/Auth";
function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Auth />} />
      <Route path="/chat" element={<Chat />} />
    </Routes>
  );
}

export default AppRouter;