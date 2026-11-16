import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { api } from '../services/api';

export default function AdminDashboard({ user, onLogout }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProjects() {
      const data = await api.getProjects();
      setProjects(data.projects || []);
      setLoading(false);
    }
    fetchProjects().catch((err) => console.error(err));
  }, []);

  const stats = useMemo(() => {
    const published = projects.filter((p) => p.review_status === 'published').length;
    const total = projects.length;
    return { total, published };
  }, [projects]);

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={onLogout || (() => window.location.href = '/login')} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <h1>Admin Dashboard</h1>
          {loading ? <div className="empty-state">Loading dashboard...</div> : (
            <>
              <div className="stats-grid">
                <div className="stat-card">
                  <span>Total Projects</span>
                  <strong>{stats.total}</strong>
                </div>
                <div className="stat-card">
                  <span>Published</span>
                  <strong>{stats.published}</strong>
                </div>
                <div className="stat-card">
                  <span>Pending Notes</span>
                  <strong>{projects.filter((p) => p.review_status === 'draft').length}</strong>
                </div>
              </div>

              <div className="section-card">
                <div className="section-title-row">
                  <h3>Recent Projects</h3>
                  <Link to="/admin/projects" className="btn">Manage Projects</Link>
                </div>
                <div className="project-list">
                  {projects.slice(0, 5).map((project) => (
                    <div key={project.id} className="project-item">
                      <div>
                        <h4>{project.name}</h4>
                        <p>{project.description}</p>
                      </div>
                      <div className="project-meta">
                        <span className={`badge ${project.review_status}`}>{project.review_status}</span>
                        <Link to={`/admin/projects/${project.id}`}>Open</Link>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  );
}
