import { Navigate ,Outlet } from "react-router-dom";
import { isAuthenticated } from "../utils/auth";


function ProtectedRoute() {
  const token = localStorage.getItem("access_token");

  if (!token) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}



export default ProtectedRoute;