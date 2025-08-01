import { Link } from 'react-router-dom';
import '../styles/Profile.css';
//profile
export default function Profile() {
  return (
    <div className="profile-page">
      <div className="left-section">
        <div className="user-info">
          <div className="profile-photo" />
          <div className="user-details">
            <h2>Nome da Pessoa</h2>
            <p>@username</p>
            <p>Endereço: Rua Exemplo, 123</p>
            <p>Telefone: (99) 99999-9999</p>
            <p>Email: exemplo@email.com</p>
          </div>
        </div>

        <div className="user-settings">
          <h3>Configurações</h3>
          <ul>
            <li>Alterar Senha</li>
            <li>Atualizar Foto</li>
            <li>
              <Link to="/" className="back-to-home-button"> Voltar para Doações</Link>
            </li>
          </ul>
        </div>
      </div>

      <div className="right-section">
        <div className="donations-box">
          <h3>Donations</h3>
          <p>Últimas doações feitas</p>
          <div className="donation-grid">
            {[...Array(8)].map((_, i) => (
              <div className="donation-card" key={i}>
                <div className="donation-photo" />
                <p>Nome do Item</p>
                <span>Data</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
