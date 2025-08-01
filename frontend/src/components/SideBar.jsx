import '../styles/Sidebar.css';
import { Link } from 'react-router-dom'

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <h2>A&D</h2>
      <ul>
     
        <li><Link to="/anunciar" className="sidebar-button destaque">Fazer um Anúncio</Link></li>
        <li><Link to="/chat">Bate Papo</Link></li>
        <li><Link to="/profile">Perfil</Link></li>
        <li><Link to="/login">Sair</Link></li>
      </ul>
    </aside>
  );
}
