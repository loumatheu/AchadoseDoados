// routes/Login.jsx
import { useNavigate } from 'react-router-dom';
import '../styles/Auth.css';
//login
export default function Login() {
  const navigate = useNavigate();

  const handleLogin = () => {
    // Aqui você faria a verificação real
    navigate('/');
  };

  return (
    <div className="auth-page">
      <div className="auth-box">
        <h1>A&D</h1>
        <h2>Login</h2>
        <input type="text" placeholder="Nome de Usuário" />
        <input type="password" placeholder="Senha" />
        <button onClick={handleLogin}>Entrar</button>
        <p>Não tem uma conta? <span onClick={() => navigate('/register')}>Cadastre-se</span></p>
      </div>
    </div>
  );
}
