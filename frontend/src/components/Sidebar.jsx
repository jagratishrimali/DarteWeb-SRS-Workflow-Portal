import { Link } from 'react-router-dom';

export default function Sidebar({ user }) {
  const isAdmin = user?.role === 'admin';

  return (
    <aside className="sidebar">
      <nav>
        {isAdmin ? (
          <>
            <Link to="/admin">Dashboard</Link>
            <Link to="/admin/projects">Projects</Link>
          </>
        ) : (
          <>
            <Link to="/client">Dashboard</Link>
            <Link to="/client/comments">My Comments</Link>
          </>
        )}
      </nav>
    </aside>
  );
}
