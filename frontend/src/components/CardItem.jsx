import '../styles/CardItem.css';

export default function CardItem({ item }) {
  return (
    <div className="card-item">
      <div className="item-image-section">
        <img src={item.foto} alt={item.nome} className="item-image" />
        <p className="item-nome">{item.nome}</p>
      </div>

      <div className="item-info-section">
        <p><strong>Endereço:</strong> {item.endereco}</p>
        <p><strong>Tempo de uso:</strong> {item.tempoUso}</p>
        <p><strong>Condição:</strong> {item.condicao}</p>
        <p><strong>Status:</strong> {item.status}</p>
        <p><strong>Classificação:</strong> {item.classificacao}</p>
      </div>

      <div className="user-section">
        <img src={item.usuarioFoto} alt="Usuário" className="user-image" />
        <p className="user-nome">{item.usuarioNome}</p>
      </div>
    </div>
  );
}
