import CardItem from './CardItem';

export default function TestPage() {
  const item = {
    foto: "https://via.placeholder.com/150",
    nome: "Geladeira Brastemp",
    endereco: "Rua das Flores, 123",
    tempoUso: "2 anos",
    condicao: "Semi-novo",
    status: "Disponível",
    classificacao: "Eletrodoméstico",
    usuarioFoto: "https://via.placeholder.com/50",
    usuarioNome: "Maria Oliveira"
  };

  return (
    <div style={{ padding: '20px' }}>
      <CardItem item={item} />
    </div>
  );
}
