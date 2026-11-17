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
  const [message, setMessage] = useState('');

  const fetchSteps = async () => {
    const data = await api.getProjectSteps(id);
    setSteps(data.steps || []);
  };

  useEffect(() => {
    fetchSteps().catch((err) => setMessage(err.message));
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const payload = { project_id: Number(id), ...form };
      if (editingId) {
        await api.updateStep(editingId, payload);
        setEditingId(null);
      } else {
        await api.createStep(payload);
      }
      setForm({ title: '', description: '' });
      await fetchSteps();
      setMessage('Workflow step saved.');
    } catch (err) {
      setMessage(err.message === 'Admin role required'
        ? 'This session is not an admin session. Log out and sign in with the admin account.'
        : err.message);
    }
  };

  const handleEdit = (step) => {
    setEditingId(step.id);
    setForm({ title: step.title, description: step.description });
  };

  const handleDelete = async (stepId) => {
    if (!window.confirm('Delete step?')) return;
    try {
      await api.deleteStep(stepId);
      await fetchSteps();
      setMessage('Workflow step deleted.');
    } catch (err) {
      setMessage(err.message);
    }
  };

  const moveStep = async (step, direction) => {
    const nextOrder = [...steps].sort((a, b) => a.sequence - b.sequence);
    const currentIndex = nextOrder.findIndex((s) => s.id === step.id);
    const swapIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;
    if (swapIndex < 0 || swapIndex >= nextOrder.length) return;
    const updated = [...nextOrder];
    [updated[currentIndex], updated[swapIndex]] = [updated[swapIndex], updated[currentIndex]];
    const orderedIds = updated.map((s) => s.id);
    try {
      await api.reorderSteps(id, orderedIds);
      await fetchSteps();
      setMessage('Workflow order updated.');
    } catch (err) {
      setMessage(err.message);
    }
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
              {message && (
                <div className={['Workflow step saved.', 'Workflow step deleted.', 'Workflow order updated.'].includes(message) ? 'success-box' : 'error-box'} role="status">
                  {message}
                </div>
              )}
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
