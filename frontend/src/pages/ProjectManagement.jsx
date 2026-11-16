import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { api } from '../services/api';

export default function ProjectManagement({ user, onLogout }) {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [form, setForm] = useState({ name: '', description: '', srs_content: '' });
  const [message, setMessage] = useState('');

  const fetchProjects = async () => {
    try {
      const data = await api.getProjects();
      setProjects(data.projects || []);
    } catch (err) {
      setMessage(err.message);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.createProject(form);
      setForm({ name: '', description: '', srs_content: '' });
      await fetchProjects();
      setMessage('Project created successfully');
    } catch (err) {
      setMessage(err.message);
    }
  };

  const handleDelete = async (projectId) => {
    if (!window.confirm('Delete this project?')) return;
    try {
      await api.deleteProject(projectId);
      await fetchProjects();
    } catch (err) {
      setMessage(err.message);
    }
  };

  const handlePublish = async (projectId) => {
    try {
      await api.publishProject(projectId);
      await fetchProjects();
      setMessage('Project published');
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={onLogout || (() => navigate('/login'))} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <h1>Project Management</h1>
          <div className="panel-grid">
            <form className="card form-card" onSubmit={handleSubmit}>
              <h3>Create Project</h3>
              <label>
                Name
                <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
              </label>
              <label>
                Description
                <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} required />
              </label>
              <label>
                SRS Content
                <textarea value={form.srs_content} onChange={(e) => setForm({ ...form, srs_content: e.target.value })} required />
              </label>
              <button className="btn" type="submit">Save Project</button>
              {message && <div className="success-box">{message}</div>}
            </form>

            <div className="card">
              <h3>Projects</h3>
              <div className="project-list compact">
                {projects.map((project) => (
                  <div key={project.id} className="project-item">
                    <div>
                      <h4>{project.name}</h4>
                      <p>{project.description}</p>
                    </div>
                    <div className="project-actions">
                      <span className={`badge ${project.review_status}`}>{project.review_status}</span>
                      <Link to={`/admin/projects/${project.id}`}>View</Link>
                      <button className="btn small" onClick={() => handlePublish(project.id)}>Publish</button>
                      <button className="btn danger small" onClick={() => handleDelete(project.id)}>Delete</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
