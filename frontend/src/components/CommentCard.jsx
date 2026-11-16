export default function CommentCard({ comment, onReview, adminMode = false }) {
  return (
    <div className="comment-card">
      <div className="comment-topline">
        <strong>{comment.client?.username || 'Client'}</strong>
        <span className={`badge ${comment.status}`}>{comment.status}</span>
      </div>
      <p className="muted">Step: {comment.workflow_step?.title || 'Unknown step'}</p>
      <p>{comment.body}</p>
      <div className="meta-row">
        <small>{new Date(comment.created_at).toLocaleString()}</small>
      </div>
      {comment.admin_response && (
        <div className="response-box">
          <strong>Admin response:</strong> {comment.admin_response}
        </div>
      )}
      {adminMode && comment.status === 'pending' && (
        <div className="review-actions">
          <button className="btn" onClick={() => onReview(comment.id, 'accepted')}>Accept</button>
          <button className="btn secondary" onClick={() => onReview(comment.id, 'rejected')}>Reject</button>
        </div>
      )}
    </div>
  );
}
