import React, { useEffect, useState, useRef } from 'react';
import '../styles/ChatPage.css';

const mockUsers = [
  { id: 1, name: 'João Silva', photo: 'https://via.placeholder.com/40' },
  { id: 2, name: 'Maria Souza', photo: 'https://via.placeholder.com/40' },
];

export default function ChatPage() {
  const [selectedUser, setSelectedUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const socketRef = useRef(null);

  useEffect(() => {
    // Supondo que seu backend escute nesse endereço
    socketRef.current = new WebSocket('ws://localhost:8080');

    socketRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prev) => [...prev, message]);
    };

    return () => socketRef.current.close();
  }, []);

  const handleSendMessage = () => {
    if (newMessage && selectedUser) {
      const msg = {
        to: selectedUser.id,
        content: newMessage,
        timestamp: new Date(),
        fromMe: true,
      };
      socketRef.current.send(JSON.stringify(msg));
      setMessages((prev) => [...prev, msg]);
      setNewMessage('');
    }
  };

  return (
    <div className="chat-page">
      <aside className="chat-sidebar">
  <div className="chat-back-button">
    <a href="/" className="custom-back-link">Voltar para Doações</a>
  </div>
  <h2>Conversas</h2>
  {mockUsers.map((user) => (
    <div
      key={user.id}
      className={`chat-user ${selectedUser?.id === user.id ? 'active' : ''}`}
      onClick={() => setSelectedUser(user)}
    >
      <img src={user.photo} alt={user.name} />
      <span>{user.name}</span>
    </div>
  ))}
</aside>

      <section className="chat-window">
        {selectedUser ? (
          <>
            <header className="chat-header">{selectedUser.name}</header>
            <div className="chat-messages">
              {messages
                .filter((msg) => msg.to === selectedUser.id || msg.from === selectedUser.id)
                .map((msg, index) => (
                  <div
                    key={index}
                    className={`chat-bubble ${msg.fromMe ? 'me' : 'them'}`}
                  >
                    {msg.content}
                  </div>
                ))}
            </div>
            <div className="chat-input">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Digite sua mensagem..."
              />
              <button onClick={handleSendMessage}>Enviar</button>
            </div>
          </>
        ) : (
          <p className="no-user">Selecione uma conversa</p>
        )}
      </section>
    </div>
  );
}
