import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../../contexts/AuthContext";

function ProtectedRoute({ children, roles = [] }) {
  const { user } = useContext(AuthContext);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (roles.length && !roles.some(role => user.roles.includes(role))) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default ProtectedRoute;
