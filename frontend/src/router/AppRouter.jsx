import { Routes, Route } from "react-router-dom";

import Auth from "../pages/Auth/Auth";
import Chat from "../pages/Chat/Chat";
import ProtectedRoute from "./ProtectedRoute";

function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Auth />} />

      <Route
        path="/chat"
        element={
          <ProtectedRoute>
            <Chat />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default AppRouter;