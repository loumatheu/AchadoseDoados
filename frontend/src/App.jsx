import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Home from './routes/Home';
import ItemDetail from './routes/ItemDetails';
import Profile from './routes/Profile';
import Navbar from './components/Navbar';
import Login from './routes/Login';
import Register from './routes/Register';
import ChatPage from './routes/ChatPage';
import Anunciar from './routes/Anunciar';



//att
function AppContent() {
  const location = useLocation();
  const hideNavbar = location.pathname === '/login' || location.pathname === '/register';

  return (
    <>
      {!hideNavbar && <Navbar />}
      <Routes>
        <Route path="/chat/:usuarioId" element={<ChatPage />} />
        <Route path="/anunciar" element={<Anunciar />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Home />} />
        <Route path="/item/:id" element={<ItemDetail />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}
