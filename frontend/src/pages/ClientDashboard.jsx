import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { api } from '../services/api';

export default function ClientDashboard({ user, onLogout }) {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    async function fetchProjects() {
      const data = await api.getProjects();
      setProjects(data.projects || []);
    }
    fetchProjects().catch((err) => console.error(err));
  }, []);

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={onLogout} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <h1>Client Dashboard</h1>
          <div className="project-list">
            {projects.length === 0 ? (
              <div className="empty-state">No published projects are available yet.</div>
            ) : (
              projects.filter((p) => p.review_status === 'published').map((project) => (
                <div key={project.id} className="project-item large">
                  <div>
                    <h3>{project.name}</h3>
                    <p>{project.description}</p>
                  </div>
                  <Link className="btn" to={`/client/projects/${project.id}`}>Open Review</Link>
                </div>
              ))
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
