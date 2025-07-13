const express = require('express');
const axios = require('axios');
const cron = require('node-cron');

const app = express();
app.use(express.json());

// Configurações
const CONFIG = {
    port: 3001,
    pythonApiUrl: 'http://localhost:8000/api',
    emailService: {
        // Configurações do serviço de email (pode ser SendGrid, Nodemailer, etc.)
        enabled: false
    }
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
app.post('/notifications/send', async (req, res) => {
    try {
        const { type, recipient, data, priority = 'normal' } = req.body;
        
        if (!type || !recipient || !data) {
            return res.status(400).json({
                error: 'Campos obrigatórios: type, recipient, data'
            });
        }

        const notification = {
            id: generateId(),
            type,
            recipient,
            data,
            priority,
            status: 'pending',
            createdAt: new Date().toISOString(),
            attempts: 0
        };

        notificationQueue.push(notification);
        
        // Processar notificação imediatamente se for alta prioridade
        if (priority === 'high') {
            await processNotification(notification);
        }

        res.json({
            message: 'Notificação adicionada à fila',
            notificationId: notification.id
        });
    } catch (error) {
        console.error('Erro ao processar notificação:', error);
        res.status(500).json({ error: 'Erro interno do servidor' });
    }
});

// Endpoint para consultar status de notificação
app.get('/notifications/:id', (req, res) => {
    const { id } = req.params;
    
    const notification = notificationHistory.find(n => n.id === id) || 
                        notificationQueue.find(n => n.id === id);
    
    if (!notification) {
        return res.status(404).json({ error: 'Notificação não encontrada' });
    }
    
    res.json(notification);
});

// Endpoint para listar todas as notificações
app.get('/notifications', (req, res) => {
    const { status, type, limit = 50 } = req.query;
    
    let notifications = [...notificationHistory, ...notificationQueue];
    
    // Filtros
    if (status) {
        notifications = notifications.filter(n => n.status === status);
    }
    
    if (type) {
        notifications = notifications.filter(n => n.type === type);
    }
    
    // Ordenar por data de criação (mais recente primeiro)
    notifications.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    
    // Limitar resultados
    notifications = notifications.slice(0, parseInt(limit));
    
    res.json({
        notifications,
        total: notifications.length
    });