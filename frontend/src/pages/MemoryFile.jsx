import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import { api } from '../services/api';

export default function MemoryFile({ user, onLogout }) {
  const { id } = useParams();
  const [entries, setEntries] = useState([]);

  useEffect(() => {
    async function fetchEntries() {
      const data = await api.getMemory(id);
      setEntries(data.memory_entries || []);
    }
    fetchEntries().catch((err) => console.error(err));
  }, [id]);

  const exportFile = () => {
    window.open(api.exportMemory(id), '_blank');
  };

  return (
    <div className="app-shell">
      <Navbar user={user} onLogout={onLogout} />
      <div className="main-layout">
        <Sidebar user={user} />
        <main className="content-panel">
          <div className="section-title-row">
            <h1>Memory File</h1>
            <button className="btn" onClick={exportFile}>Export Markdown</button>
          </div>

          {entries.length === 0 ? (
            <div className="empty-state">No approved feedback in the Memory File yet.</div>
          ) : (
            <div className="comment-list">
              {entries.map((entry) => (
                <div className="comment-card" key={entry.id}>
                  <div className="comment-topline">
                    <strong>Step: {entry.step_title}</strong>
                    <span className="badge accepted">Accepted</span>
                  </div>
                  <p>{entry.approved_text}</p>
                  <p className="muted">Approved by Admin ID {entry.approved_by}</p>
                  <small>{entry.approved_at ? new Date(entry.approved_at).toLocaleString() : 'N/A'}</small>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
