import { useParams, useNavigate } from 'react-router-dom';
import '../styles/ItemDetails.css';

export default function ItemDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  // Exemplo de dados fictícios (substituir por fetch futuramente)
  const item = {
    nome: 'Botas de Borracha',
    descricao: 'Botas usadas, em perfeito estado, pouco uso e poucas marcas.',
    endereco: 'Casa Amarela - Recife',
    tempoDeUso: '6 meses',
    condicao: 'Muito boa',
    status: 'Disponível',
    classificacao: 'Calçados',
    foto: 'https://via.placeholder.com/250',
    usuario: {
      id: '123', // <-- ID que será usado na rota do chat
      nome: 'João Silva',
      foto: 'https://via.placeholder.com/50'
    }
  };

  const irParaChat = () => {
    navigate(`/chat/${item.usuario.id}`);
  };

  return (
    <div className="item-detail-wrapper">
      <a href="/" className="back-to-home-button">Voltar para Doações</a>

      <div className="item-detail-container">
        {/* Esquerda */}
        <div className="item-left">
          <img src={item.foto} alt={item.nome} className="item-img" />
          <h2>{item.nome}</h2>
        </div>

        {/* Direita */}
        <div className="item-right">
          <div className="user-info">
            <img src={item.usuario.foto} alt="Usuário" className="user-photo" />
            <p className="user-name">{item.usuario.nome}</p>
          </div>
          <p><strong>Descrição:</strong> {item.descricao}</p>
          <p><strong>Endereço:</strong> {item.endereco}</p>
          <p><strong>Tempo de uso:</strong> {item.tempoDeUso}</p>
          <p><strong>Condição:</strong> {item.condicao}</p>
          <p><strong>Status:</strong> {item.status}</p>
          <p><strong>Classificação:</strong> {item.classificacao}</p>
        </div>

        {/* Botões */}
        <div className="buttons-container">
          <button className="btn-red">Gostar</button>
          <button className="btn-blue" onClick={irParaChat}>Chat</button>
        </div>
      </div>
    </div>
  );
}
