import { useCallback, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import WorkflowSteps from '../components/WorkflowSteps';
import { api } from '../services/api';

export default function ClientProjectView({ user, onLogout }) {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [steps, setSteps] = useState([]);
  const [comments, setComments] = useState([]);
  const [selectedStep, setSelectedStep] = useState('');
  const [commentBody, setCommentBody] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const fetchData = useCallback(async () => {
    const projectData = await api.getProjects();
    const found = (projectData.projects || []).find((p) => p.id === Number(id));
    setProject(found || null);
    const stepData = await api.getProjectSteps(id);
    setSteps(stepData.steps || []);
    const commentData = await api.getProjectComments(id);
    setComments(commentData.comments || []);
    setError('');
  }, [id]);

  useEffect(() => {
    const refresh = () => fetchData().catch((err) => setError(err.message));
    refresh();
    const intervalId = window.setInterval(refresh, 30000);
    window.addEventListener('focus', refresh);

    return () => {
      window.clearInterval(intervalId);
      window.removeEventListener('focus', refresh);
    };
  }, [fetchData]);

  const handleSubmitComment = async (e) => {
    e.preventDefault();
    if (!selectedStep) return alert('Select a workflow step');
    try {
      await api.submitComment({ step_id: Number(selectedStep), body: commentBody });
      setCommentBody('');
      setSelectedStep('');
      setMessage('Comment submitted. It will remain Pending until an admin reviews it.');
      await fetchData();
    } catch (err) {
      setError(err.message);
    }
  };

  if (!project) return <div className="empty-state">Loading project...</div>;

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={onLogout} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <h1>{project.name}</h1>
          <div className="card">
            <h3>SRS Summary</h3>
            <pre className="code-block">{project.srs_content}</pre>
          </div>

          <div className="panel-grid">
            <div className="card">
              <h3>Workflow</h3>
              <WorkflowSteps steps={steps} />
            </div>

            <form className="card form-card" onSubmit={handleSubmitComment}>
              <h3>Submit comment</h3>
              <label>
                Workflow Step
                <select value={selectedStep} onChange={(e) => setSelectedStep(e.target.value)} required>
                  <option value="">Select step</option>
                  {steps.map((step) => (
                    <option key={step.id} value={step.id}>{step.title}</option>
                  ))}
                </select>
              </label>
              <label>
                Comment
                <textarea value={commentBody} onChange={(e) => setCommentBody(e.target.value)} required />
              </label>
              <button className="btn" type="submit">Submit Comment</button>
            </form>
          </div>

          <div className="card">
            <div className="section-title-row">
              <h3>My Status</h3>
              <button className="btn secondary" type="button" onClick={() => fetchData().catch((err) => setError(err.message))}>
                Refresh status
              </button>
            </div>
            {message && <div className="success-box" role="status">{message}</div>}
            {error && <div className="error-box" role="alert">{error}</div>}
            {comments.length === 0 ? (
              <div className="empty-state">You have not submitted comments yet.</div>
            ) : (
              <div className="comment-list">
                {comments.map((comment) => (
                  <div key={comment.id} className="comment-card">
                    <div className="comment-topline">
                      <strong>{comment.workflow_step?.title}</strong>
                      <span className={`badge ${comment.status}`}>{comment.status}</span>
                    </div>
                    <p>{comment.body}</p>
                    {comment.admin_response && <p className="response-box">Admin: {comment.admin_response}</p>}
                  </div>
                ))}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
