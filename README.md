# Achados & Doados
## Tecnologias Principais
### Backend Python (FastAPI)
---
- **FastAPI**: Framework principal para a API
- **Pydantic**: Validação de dados
- **SQLAlchemy**: ORM (pode ser usado mesmo com JSON local)
- **Python-multipart**: Para upload de arquivos
- **Uvicorn**: Servidor ASGI

### Backend JavaScript
---
- **Express.js**: Para serviços auxiliares
- **Sharp**: Processamento de imagens
- **Node-cron**: Para tarefas agendadas
- **Axios**: Cliente HTTP para comunicação entre serviços

# Módulos
### 1. Módulo de Gerenciamento de Itens (Python)
- Cadastro de itens para doação
- Busca e filtros
- Categorização
- Status do item (disponível, reservado, doado)

### 2. Módulo de Usuários (Python)
- Cadastro de doadores e receptores
- Autenticação básica
- Perfil do usuário
- Histórico de doações

### 3. Módulo de Doações (Python)
- Processo de solicitação
- Matching entre doadores e receptores
- Status da doação
- Histórico completo

### 4. Módulo de Notificações (JavaScript)
- Sistema de notificações em tempo real
- Emails automáticos (nodemailer)
- Notificações push (possível implementação no futuro)

### 5. Módulo de Chat (Python)
- Comunicação direta entre doador e receptor
- Histórico de conversas
- Integração com o sistema de notificações (possivelmente)

### 6. Módulo de Frontend (React JS)
- Interface para todas as interações do usuário
- Integração com todos os módulos via API
- Design responsívo

### 7. Módulo de Geolocalização 
- Distância entre usuários
- Conversão de CEP para coordenadas geográficas

### 8. Módulo de Avaliação
- Criar uma nova avaliação
- Obter todas as avaliações recebidas por um usuário
- Calcular a reputação do usuário


## Configurações do Projeto
### Configurar ambiente Python
```bash
cd backend/python-api
python -m venv venv
source venv/bin/activate # Linux
```
### ou
```bash
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Configurar ambiente JavaScript
```bash
# Instalação de Dependências (Linux):
# 1. Download do NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash

# 2. Reiniciar o terminal
\. "$HOME/.nvm/nvm.sh"

# 3. Download do Node.js
nvm install 22 # Versão LTS

# Verificando a instalação do Node
node -v

# 4. Instalando dependências
cd ../js-services
npm install
```

## Executar a API Python
```bash
cd ../python-api
uvicorn app.main:app --reload
```

## Executar serviços JavaScript
```bash
cd ../js-services
npm run dev
```

## Criação de Tabelas:

Execute o seguinte comando na pasta python-api:
```python
python3 -m app.createtables
```
