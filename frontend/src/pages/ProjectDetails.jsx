import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { api } from '../services/api';

export default function ProjectDetails({ user, onLogout }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [form, setForm] = useState({ name: '', description: '', srs_content: '' });

  useEffect(() => {
    async function fetchProject() {
      const data = await api.getProjects();
      const found = (data.projects || []).find((p) => p.id === Number(id));
      if (found) {
        setProject(found);
        setForm({
          name: found.name,
          description: found.description,
          srs_content: found.srs_content,
        });
      }
    }
    fetchProject().catch((err) => console.error(err));
  }, [id]);

  const handleUpdate = async (e) => {
    e.preventDefault();
    await api.updateProject(id, form);
    const data = await api.getProjects();
    setProject((data.projects || []).find((p) => p.id === Number(id)));
    alert('Project updated');
  };

  if (!project) return <div className="empty-state">Loading project...</div>;

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={onLogout || (() => navigate('/login'))} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <div className="section-title-row">
            <h1>{project.name}</h1>
            <div className="inline-actions">
              <Link className="btn secondary" to={`/admin/projects/${id}/workflow`}>Workflow</Link>
              <Link className="btn secondary" to={`/admin/projects/${id}/comments`}>Comments</Link>
              <Link className="btn secondary" to={`/admin/projects/${id}/memory`}>Memory</Link>
            </div>
          </div>

          <form className="card form-card" onSubmit={handleUpdate}>
            <h3>Edit Project</h3>
            <label>
              Name
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </label>
            <label>
              Description
              <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
            </label>
            <label>
              SRS Content
              <textarea value={form.srs_content} onChange={(e) => setForm({ ...form, srs_content: e.target.value })} />
            </label>
            <button className="btn" type="submit">Update Project</button>
          </form>

          <div className="card">
            <h3>Project Summary</h3>
            <p>{project.description}</p>
            <pre className="code-block">{project.srs_content}</pre>
          </div>
        </main>
      </div>
    </div>
  );
}
