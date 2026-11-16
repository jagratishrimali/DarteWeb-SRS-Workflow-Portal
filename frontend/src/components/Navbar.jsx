import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function Navbar({ user, onLogout }) {
  const handleLogout = async () => {
    try {
      await api.logout();
      onLogout();
    } catch (error) {
      console.error(error);
      onLogout();
    }
  };

  return (
    <header className="topbar">
      <div>
        <h2>SRS Review Portal</h2>
      </div>
      <div className="topbar-right">
        <span className="user-pill">{user?.role === 'admin' ? 'Admin' : 'Client'} · {user?.username}</span>
        <button className="btn secondary" onClick={handleLogout}>Logout</button>
      </div>
    </header>
  );
}
