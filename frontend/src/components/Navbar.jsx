import { useNavigate } from 'react-router-dom';


export default function Navbar() {
  const navigate = useNavigate();

  return (
    <header style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem', border:'solid 1px black', background: '#d6f7f2ff', height:'50px' }}>
      <h1>A&D</h1>
      <button onClick={() => navigate('/profile')} style={{ borderRadius: '50%', width: 40, height: 40, background: 'black' }} />
    </header>
  );
}
