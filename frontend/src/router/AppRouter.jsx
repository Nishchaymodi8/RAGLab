import { Routes, Route } from "react-router-dom";

import Chat from "../pages/chat/chat";

function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Chat />} />
    </Routes>
  );
}

export default AppRouter;