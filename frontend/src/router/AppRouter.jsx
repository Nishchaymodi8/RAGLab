import { Routes, Route } from "react-router-dom";

import Auth from "../pages/Auth/Auth";
import Chat from "../pages/chat/chat";
import ProtectedRoute from "./ProtectedRoute";
import Settings from "../pages/Settings/Settings";
import Documents from "../pages/Documents/Documents";
import Lab from "../pages/Lab/Lab";


function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Auth />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/chat" element={<Chat />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/lab" element={<Lab />} />
      </Route>
    </Routes>
  );
}

export default AppRouter;