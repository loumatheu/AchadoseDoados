// backend/Chat/src/index.js
const WebSocket = require('ws');
const jwt = require('jsonwebtoken');
require('dotenv').config();

const wss = new WebSocket.Server({ port: 8080 }, () => {
  console.log('Servidor WebSocket rodando na porta 8080');
});

wss.on('connection', (ws, req) => {
  const params = new URLSearchParams(req.url.split('?')[1]);
  const token = params.get('token');
  const room = params.get('room');

  let userId;
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET || 'secretao');
    userId = payload.id;
  } catch (e) {
    ws.send(JSON.stringify({ error: 'Token inválido' }));
    ws.close();
    return;
  }

  console.log(`Usuário ${userId} conectado à sala ${room}`);

  ws.on('message', (msg) => {
    const mensagem = JSON.parse(msg);
    console.log(`[Sala ${room}] ${userId}: ${mensagem.text}`);
    // Aqui você pode broadcast para todos na mesma sala (se tiver múltiplos clientes)
    ws.send(JSON.stringify({ self: true, text: mensagem.text }));
  });

  ws.send(JSON.stringify({ system: true, text: 'Bem-vindo ao chat!' }));
});
