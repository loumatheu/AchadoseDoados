import { useNavigate } from 'react-router-dom';
import CardItem from '../components/CardItem';
import '../styles/Home.css';
import Sidebar from '../components/SideBar'; 
//home
const mockData = [
  { id: 1, title: 'Botas semi novas', description: 'Botas de borracha', image: '"C:\\Users\\ruang\\Documents\\app\\SistemasDistribuidos\\frontend\\src\\imagens\\botas de borracha.webp"' },
  { id: 2, title: 'Outro item', description: 'Descrição curta', image: 'https://via.placeholder.com/150' },
];

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-layout">
      <Sidebar />
      <div className="cards-wrapper">
        {mockData.map(item => (
          <div key={item.id} onClick={() => navigate(`/item/${item.id}`)}>
            <CardItem item={item} />
          </div>
        ))}
      </div>
    </div>
  );
}
