import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import WorkflowSteps from '../components/WorkflowSteps';
import { api } from '../services/api';

export default function WorkflowManagement({ user, onLogout }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [steps, setSteps] = useState([]);
  const [form, setForm] = useState({ title: '', description: '' });
  const [editingId, setEditingId] = useState(null);

  const fetchSteps = async () => {
    const data = await api.getProjectSteps(id);
    setSteps(data.steps || []);
  };

  useEffect(() => {
    fetchSteps().catch((err) => console.error(err));
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = { project_id: Number(id), ...form };
    if (editingId) {
      await api.updateStep(editingId, payload);
      setEditingId(null);
    } else {
      await api.createStep(payload);
    }
    setForm({ title: '', description: '' });
    await fetchSteps();
  };

  const handleEdit = (step) => {
    setEditingId(step.id);
    setForm({ title: step.title, description: step.description });
  };

  const handleDelete = async (stepId) => {
    if (!window.confirm('Delete step?')) return;
    await api.deleteStep(stepId);
    await fetchSteps();
  };

  const moveStep = async (step, direction) => {
    const nextOrder = [...steps].sort((a, b) => a.sequence - b.sequence);
    const currentIndex = nextOrder.findIndex((s) => s.id === step.id);
    const swapIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;
    if (swapIndex < 0 || swapIndex >= nextOrder.length) return;
    const updated = [...nextOrder];
    [updated[currentIndex], updated[swapIndex]] = [updated[swapIndex], updated[currentIndex]];
    const orderedIds = updated.map((s) => s.id);
    await api.reorderSteps(id, orderedIds);
    await fetchSteps();
  };

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={() => navigate('/login')} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <h1>Workflow Management</h1>
          <div className="panel-grid">
            <form className="card form-card" onSubmit={handleSubmit}>
              <h3>{editingId ? 'Edit Step' : 'Add Workflow Step'}</h3>
              <label>
                Title
                <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
              </label>
              <label>
                Description
                <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} required />
              </label>
              <div className="inline-actions">
                <button className="btn" type="submit">{editingId ? 'Save Changes' : 'Add Step'}</button>
                {editingId && <button className="btn secondary" type="button" onClick={() => { setEditingId(null); setForm({ title: '', description: '' }); }}>Cancel</button>}
              </div>
            </form>

            <div className="card">
              <h3>Current Workflow</h3>
              <WorkflowSteps
                steps={steps}
                showActions
                onMoveUp={(step) => moveStep(step, 'up')}
                onMoveDown={(step) => moveStep(step, 'down')}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
