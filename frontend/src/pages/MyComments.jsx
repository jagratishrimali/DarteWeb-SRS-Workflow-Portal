import { useCallback, useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { api } from '../services/api';

export default function MyComments({ user, onLogout }) {
  const [comments, setComments] = useState([]);
  const [error, setError] = useState('');

  const fetchComments = useCallback(async () => {
    const data = await api.getMyComments();
    setComments(data.comments || []);
    setError('');
  }, []);

  useEffect(() => {
    const refresh = () => fetchComments().catch((err) => setError(err.message));
    refresh();
    const intervalId = window.setInterval(refresh, 30000);
    window.addEventListener('focus', refresh);

    return () => {
      window.clearInterval(intervalId);
      window.removeEventListener('focus', refresh);
    };
  }, [fetchComments]);

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={onLogout} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <div className="section-title-row">
            <h1>My Comments</h1>
            <button className="btn secondary" onClick={() => fetchComments().catch((err) => setError(err.message))}>
              Refresh
            </button>
          </div>
          {error && <div className="error-box" role="alert">{error}</div>}
          {comments.length === 0 ? (
            <div className="empty-state">No comments submitted yet.</div>
          ) : (
            <div className="comment-list">
              {comments.map((comment) => (
                <div className="comment-card" key={comment.id}>
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
        </main>
      </div>
    </div>
  );
}
