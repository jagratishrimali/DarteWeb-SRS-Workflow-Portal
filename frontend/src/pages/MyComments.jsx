import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { api } from '../services/api';

export default function MyComments({ user, onLogout }) {
  const [comments, setComments] = useState([]);

  useEffect(() => {
    async function fetchComments() {
      const data = await api.getMyComments();
      setComments(data.comments || []);
    }
    fetchComments().catch((err) => console.error(err));
  }, []);

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={onLogout} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <h1>My Comments</h1>
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
