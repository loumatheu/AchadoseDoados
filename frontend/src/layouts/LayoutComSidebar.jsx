
import Sidebar from '.../components/Sidebar';
import { Outlet } from 'react-router-dom';
import '../styles/LayoutComSidebar.css';

export default function LayoutComSidebar({ children }) {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <main style={{ flex: 1, padding: '1rem' }}>
        {children || <Outlet />}
      </main>
    </div>
  );
}
