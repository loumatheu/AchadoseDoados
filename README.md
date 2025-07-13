# Achados & Doados

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