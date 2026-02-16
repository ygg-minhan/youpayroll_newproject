import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom'; // Added Navigate, Outlet
import { AuthProvider, useAuth } from './context/AuthContext';
import DashboardLayout from './layouts/DashboardLayout';
import Overview from './pages/Overview';
import Placeholder from './pages/Placeholder';
import Login from './pages/Login';
import Profile from './pages/Profile';
import Payslips from './pages/Payslips';
import Wiki from './pages/Wiki';

// Protected Route Wrapper
const ProtectedRoute = () => {
  const { isAuthenticated, loading } = useAuth();

  // Show nothing while checking auth state
  if (loading) return null; // Or a spinner

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

function App() {
  return (
    <AuthProvider> {/* Wrap with Auth Provider */}
      <BrowserRouter>
        <Routes>
          {/* Public Route */}
          <Route path="/login" element={<Login />} />

          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<DashboardLayout />}>
              <Route index element={<Overview />} />
              <Route path="profile" element={<Profile />} />
              <Route path="payslips" element={<Payslips />} />
              <Route path="wiki" element={<Wiki />} />
              <Route path="documents" element={<Placeholder title="Documents" />} />
              <Route path="support" element={<Placeholder title="Support" />} />
            </Route>
          </Route>

          {/* Catch all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
