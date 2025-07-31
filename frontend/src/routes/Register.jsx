// routes/Register.jsx
import { useNavigate } from 'react-router-dom';
import '../styles/Auth.css';

export default function Register() {
  const navigate = useNavigate();

  return (
    <div className="auth-page">
      <div className="auth-box">
        <h1>A&D</h1>
        <h2>Cadastro</h2>
        <input type="email" placeholder="Email" />
        <input type="text" placeholder="Nome de Usuário" />
        <input type="text" placeholder="Endereço" />
        <input type="password" placeholder="Senha" />
        <input type="password" placeholder="Repetir Senha" />
        <button>Cadastrar</button>
        <p>Já tem uma conta? <span onClick={() => navigate('/login')}>Faça login</span></p>
      </div>
    </div>
  );
}
