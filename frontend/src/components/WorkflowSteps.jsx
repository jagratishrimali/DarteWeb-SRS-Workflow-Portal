export default function WorkflowSteps({ steps, showActions = false, onMoveUp, onMoveDown, onEdit, onDelete }) {
  if (!steps || steps.length === 0) {
    return <div className="empty-state">No workflow steps yet.</div>;
  }

  return (
    <div className="step-list">
      {steps.map((step, index) => (
        <div key={step.id} className="step-card">
          <div className="step-header">
            <span className="step-number">Step {index + 1}</span>
            {showActions && (
              <div className="inline-actions">
                <button className="btn small" onClick={() => onMoveUp(step)}>↑</button>
                <button className="btn small" onClick={() => onMoveDown(step)}>↓</button>
                <button className="btn small" onClick={() => onEdit(step)}>Edit</button>
                <button className="btn danger small" onClick={() => onDelete(step.id)}>Delete</button>
              </div>
            )}
          </div>
          <h4>{step.title}</h4>
          <p>{step.description}</p>
        </div>
      ))}
    </div>
  );
}
