const express = require("express");
const axios = require("axios");
const cron = require("node-cron");

const app = express();
app.use(express.json());

// Configurações
const CONFIG = {
  port: 3001,
  pythonApiUrl: "http://localhost:8000/api",
  emailService: {
    // Configurações do serviço de email (pode ser SendGrid, Nodemailer, etc.)
    enabled: false,
  },
};

// Simulação de banco de dados para notificações
let notificationQueue = [];
let notificationHistory = [];

// Middleware para logging
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next();
});

// Endpoint para receber notificações da API Python
app.post("/notifications/send", async (req, res) => {
  try {
    const { type, recipient, data, priority = "normal" } = req.body;

    if (!type || !recipient || !data) {
      return res.status(400).json({
        error: "Campos obrigatórios: type, recipient, data",
      });
    }

    const notification = {
      id: generateId(),
      type,
      recipient,
      data,
      priority,
      status: "pending",
      createdAt: new Date().toISOString(),
      attempts: 0,
    };

    notificationQueue.push(notification);

    // Processar notificação imediatamente se for alta prioridade
    if (priority === "high") {
      await processNotification(notification);
    }

    res.json({
      message: "Notificação adicionada à fila",
      notificationId: notification.id,
    });
  } catch (error) {
    console.error("Erro ao processar notificação:", error);
    res.status(500).json({ error: "Erro interno do servidor" });
  }
});

// Endpoint para consultar status de notificação
app.get("/notifications/:id", (req, res) => {
  const { id } = req.params;

  const notification =
    notificationHistory.find((n) => n.id === id) ||
    notificationQueue.find((n) => n.id === id);

  if (!notification) {
    return res.status(404).json({ error: "Notificação não encontrada" });
  }

  res.json(notification);
});

// Endpoint para listar todas as notificações
app.get("/notifications", (req, res) => {
  const { status, type, limit = 50 } = req.query;

  let notifications = [...notificationHistory, ...notificationQueue];

  // Filtros
  if (status) {
    notifications = notifications.filter((n) => n.status === status);
  }

  if (type) {
    notifications = notifications.filter((n) => n.type === type);
  }

  // Ordenar por data de criação (mais recente primeiro)
  notifications.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

  // Limitar resultados
  notifications = notifications.slice(0, parseInt(limit));

  res.json({
    notifications,
    total: notifications.length,
  });
});

// Endpoint para estatísticas de notificações
app.get("/notifications/stats", (req, res) => {
  const stats = {
    total: notificationHistory.length + notificationQueue.length,
    pending: notificationQueue.length,
    sent: notificationHistory.filter((n) => n.status === "sent").length,
    failed: notificationHistory.filter((n) => n.status === "failed").length,
    byType: {},
  };

  // Contar por tipo
  [...notificationHistory, ...notificationQueue].forEach((n) => {
    stats.byType[n.type] = (stats.byType[n.type] || 0) + 1;
  });

  res.json(stats);
});

// Função para processar notificação
async function processNotification(notification) {
  try {
    notification.attempts++;
    notification.lastAttempt = new Date().toISOString();

    console.log(
      `Processando notificação ${notification.id} (tentativa ${notification.attempts})`
    );

    let success = false;

    switch (notification.type) {
      case "item_interest":
        success = await sendItemInterestNotification(notification);
        break;
      case "donation_confirmed":
        success = await sendDonationConfirmedNotification(notification);
        break;
      case "new_item_match":
        success = await sendNewItemMatchNotification(notification);
        break;
      case "reminder":
        success = await sendReminderNotification(notification);
        break;
      default:
        console.warn(`Tipo de notificação desconhecido: ${notification.type}`);
        success = false;
    }

    if (success) {
      notification.status = "sent";
      notification.sentAt = new Date().toISOString();
      moveToHistory(notification);
    } else {
      notification.status = "failed";
      if (notification.attempts >= 3) {
        moveToHistory(notification);
      }
    }
  } catch (error) {
    console.error(`Erro ao processar notificação ${notification.id}:`, error);
    notification.status = "failed";
    notification.error = error.message;

    if (notification.attempts >= 3) {
      moveToHistory(notification);
    }
  }
}

// Funções específicas para cada tipo de notificação
async function sendItemInterestNotification(notification) {
  const { itemId, interestedUserId, donorId } = notification.data;

  try {
    // Buscar dados do item e usuários da API Python
    const itemResponse = await axios.get(
      `${CONFIG.pythonApiUrl}/items/${itemId}`
    );
    const userResponse = await axios.get(
      `${CONFIG.pythonApiUrl}/users/${interestedUserId}`
    );

    const item = itemResponse.data;
    const user = userResponse.data;

    // Simular envio de email/notificação
    const message = `Olá! O usuário ${user.name} demonstrou interesse no seu item "${item.title}".`;

    console.log(`[EMAIL] Para: ${notification.recipient}`);
    console.log(`[EMAIL] Assunto: Interesse no seu item`);
    console.log(`[EMAIL] Mensagem: ${message}`);

    // Aqui você integraria com um serviço real de email
    await simulateEmailSend(
      notification.recipient,
      "Interesse no seu item",
      message
    );

    return true;
  } catch (error) {
    console.error("Erro ao enviar notificação de interesse:", error);
    return false;
  }
}

async function sendDonationConfirmedNotification(notification) {
  const { donationId, itemId, donorId, recipientId } = notification.data;

  try {
    const donationResponse = await axios.get(
      `${CONFIG.pythonApiUrl}/donations/${donationId}`
    );
    const donation = donationResponse.data;

    const message = `Sua doação foi confirmada! Detalhes: ${JSON.stringify(
      donation,
      null,
      2
    )}`;

    console.log(`[EMAIL] Para: ${notification.recipient}`);
    console.log(`[EMAIL] Assunto: Doação confirmada`);
    console.log(`[EMAIL] Mensagem: ${message}`);

    await simulateEmailSend(
      notification.recipient,
      "Doação confirmada",
      message
    );

    return true;
  } catch (error) {
    console.error("Erro ao enviar notificação de doação confirmada:", error);
    return false;
  }
}

async function sendNewItemMatchNotification(notification) {
  const { itemId, userId, matchScore } = notification.data;

  try {
    const itemResponse = await axios.get(
      `${CONFIG.pythonApiUrl}/items/${itemId}`
    );
    const item = itemResponse.data;

    const message = `Encontramos um item que pode interessar você: "${item.title}". Compatibilidade: ${matchScore}%`;

    console.log(`[EMAIL] Para: ${notification.recipient}`);
    console.log(`[EMAIL] Assunto: Novo item disponível`);
    console.log(`[EMAIL] Mensagem: ${message}`);

    await simulateEmailSend(
      notification.recipient,
      "Novo item disponível",
      message
    );

    return true;
  } catch (error) {
    console.error("Erro ao enviar notificação de novo item:", error);
    return false;
  }
}

async function sendReminderNotification(notification) {
  const { message, title } = notification.data;

  try {
    console.log(`[EMAIL] Para: ${notification.recipient}`);
    console.log(`[EMAIL] Assunto: ${title || "Lembrete"}`);
    console.log(`[EMAIL] Mensagem: ${message}`);

    await simulateEmailSend(
      notification.recipient,
      title || "Lembrete",
      message
    );

    return true;
  } catch (error) {
    console.error("Erro ao enviar lembrete:", error);
    return false;
  }
}

// Função para simular envio de email
async function simulateEmailSend(recipient, subject, message) {
  // Simular delay do serviço de email
  await new Promise((resolve) => setTimeout(resolve, 100));

  // Simular falha ocasional (5% de chance)
  if (Math.random() < 0.05) {
    throw new Error("Falha simulada no serviço de email");
  }

  return true;
}

// Função para mover notificação para histórico
function moveToHistory(notification) {
  const index = notificationQueue.findIndex((n) => n.id === notification.id);
  if (index > -1) {
    notificationQueue.splice(index, 1);
    notificationHistory.push(notification);

    // Manter apenas as últimas 1000 notificações no histórico
    if (notificationHistory.length > 1000) {
      notificationHistory = notificationHistory.slice(-1000);
    }
  }
}

// Função para gerar ID único
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Processamento periódico da fila de notificações
cron.schedule("*/30 * * * * *", async () => {
  // Processar notificações pendentes a cada 30 segundos
  const pendingNotifications = notificationQueue.filter(
    (n) => n.status === "pending"
  );

  for (const notification of pendingNotifications.slice(0, 5)) {
    // Processar até 5 por vez
    await processNotification(notification);
  }
});

// Limpeza periódica de notificações antigas
cron.schedule("0 0 * * *", () => {
  // Limpar notificações antigas diariamente à meia-noite
  const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);

  notificationHistory = notificationHistory.filter(
    (n) => new Date(n.createdAt) > oneDayAgo
  );

  console.log("Limpeza de notificações antigas concluída");
});

// Health check
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    service: "notification-service",
    timestamp: new Date().toISOString(),
    stats: {
      queueSize: notificationQueue.length,
      historySize: notificationHistory.length,
    },
  });
});

// Iniciar servidor
app.listen(CONFIG.port, () => {
  console.log(`🚀 Serviço de Notificações rodando na porta ${CONFIG.port}`);
  console.log(`📧 Processamento automático ativado`);
});

// Graceful shutdown
process.on("SIGTERM", () => {
  console.log("Recebido SIGTERM. Encerrando servidor...");
  process.exit(0);
});

process.on("SIGINT", () => {
  console.log("Recebido SIGINT. Encerrando servidor...");
  process.exit(0);
});
