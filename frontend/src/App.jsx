import { Routes, Route, Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { api } from './services/api';
import Login from './pages/Login';
import AdminDashboard from './pages/AdminDashboard';
import ProjectManagement from './pages/ProjectManagement';
import ProjectDetails from './pages/ProjectDetails';
import WorkflowManagement from './pages/WorkflowManagement';
import CommentReview from './pages/CommentReview';
import MemoryFile from './pages/MemoryFile';
import ClientDashboard from './pages/ClientDashboard';
import ClientProjectView from './pages/ClientProjectView';
import MyComments from './pages/MyComments';
import ProtectedRoute from './components/ProtectedRoute';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchUser() {
      try {
        const res = await api.getMe();
        setUser(res.user);
      } catch {
        setUser(null);
      } finally {
        setLoading(false);
      }
    }

    fetchUser();
  }, []);

  const setCurrentUser = (nextUser) => setUser(nextUser);

  const handleLogout = async () => {
    try {
      await api.logout();
    } catch (error) {
      console.error(error);
    }
    setUser(null);
    window.location.href = '/login';
  };

  if (loading) {
    return <div className="app-loading">Loading portal...</div>;
  }

  return (
    <Routes>
      <Route path="/login" element={<Login onLogin={setCurrentUser} />} />

      <Route
        path="/admin"
        element={
          <ProtectedRoute user={user} allowedRoles={['admin']}>
            <AdminDashboard user={user} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/projects"
        element={
          <ProtectedRoute user={user} allowedRoles={['admin']}>
            <ProjectManagement user={user} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/projects/:id"
        element={
          <ProtectedRoute user={user} allowedRoles={['admin']}>
            <ProjectDetails user={user} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/projects/:id/workflow"
        element={
          <ProtectedRoute user={user} allowedRoles={['admin']}>
            <WorkflowManagement user={user} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/projects/:id/comments"
        element={
          <ProtectedRoute user={user} allowedRoles={['admin']}>
            <CommentReview user={user} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/projects/:id/memory"
        element={
          <ProtectedRoute user={user} allowedRoles={['admin']}>
            <MemoryFile user={user} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      <Route
        path="/client"
        element={
          <ProtectedRoute user={user} allowedRoles={['client']}>
            <ClientDashboard user={user} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      <Route
        path="/client/projects/:id"
        element={
          <ProtectedRoute user={user} allowedRoles={['client']}>
            <ClientProjectView user={user} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      <Route
        path="/client/comments"
        element={
          <ProtectedRoute user={user} allowedRoles={['client']}>
            <MyComments user={user} onLogout={handleLogout} />
          </ProtectedRoute>
        }
      />

      <Route path="/" element={user ? <Navigate to={user.role === 'admin' ? '/admin' : '/client'} replace /> : <Navigate to="/login" replace />} />
    </Routes>
  );
}
