import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import CommentCard from '../components/CommentCard';
import { api } from '../services/api';

export default function CommentReview({ user, onLogout }) {
  const { id } = useParams();
  const [comments, setComments] = useState([]);

  const fetchComments = async () => {
    const data = await api.getProjectComments(id);
    setComments(data.comments || []);
  };

  useEffect(() => {
    fetchComments().catch((err) => console.error(err));
  }, [id]);

  const handleReview = async (commentId, status) => {
    const response = window.prompt('Optional admin response:');
    try {
      await api.reviewComment(commentId, status, response || '');
      await fetchComments();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={onLogout} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <h1>Comment Review</h1>
          {comments.length === 0 ? (
            <div className="empty-state">No comments yet.</div>
          ) : (
            <div className="comment-list">
              {comments.map((comment) => (
                <CommentCard key={comment.id} comment={comment} adminMode onReview={handleReview} />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
