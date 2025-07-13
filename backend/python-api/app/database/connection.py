import json
import os
from typing import Dict, List, Any
from datetime import datetime
import uuid
from pathlib import Path

class LocalDatabase:
    def __init__(self, data_file: str = "data/local_storage.json"):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Carrega dados do arquivo JSON ou cria estrutura inicial"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return self._create_initial_structure()
        else:
            return self._create_initial_structure()
    
    def _create_initial_structure(self) -> Dict[str, Any]:
        """Cria estrutura inicial do banco de dados"""
        return {
            "items": {},
            "users": {},
            "donations": {},
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def _save_data(self):
        """Salva dados no arquivo JSON"""
        self.data["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # Criar diretório se não existir
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
    
    def generate_id(self) -> str:
        """Gera um ID único"""
        return str(uuid.uuid4())
    
    # Métodos para Items
    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo item"""
        item_id = self.generate_id()
        item_data['id'] = item_id
        item_data['created_at'] = datetime.now().isoformat()
        item_data['updated_at'] = datetime.now().isoformat()
        item_data['status'] = 'available'
        item_data['images'] = []
        item_data['interested_users'] = []
        
        self.data["items"][item_id] = item_data
        self._save_data()
        return item_data
    
    def get_item(self, item_id: str) -> Dict[str, Any] | None:
        """Busca um item pelo ID"""
        return self.data["items"].get(item_id)
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """Retorna todos os itens"""
        return list(self.data["items"].values())
    
    def update_item(self, item_id: str, update_data: Dict[str, Any]) -> Dict[str, Any] | None:
        """Atualiza um item existente"""
        if item_id not in self.data["items"]:
            return None
        
        item = self.data["items"][item_id]
        item.update(update_data)
        item['updated_at'] = datetime.now().isoformat()
        
        self.data["items"][item_id] = item
        self._save_data()
        return item
    
    def delete_item(self, item_id: str) -> bool:
        """Remove um item"""
        if item_id in self.data["items"]:
            del self.data["items"][item_id]
            self._save_data()
            return True
        return False
    
    # Métodos para Users
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo usuário"""
        user_id = self.generate_id()
        user_data['id'] = user_id
        user_data['created_at'] = datetime.now().isoformat()
        user_data['updated_at'] = datetime.now().isoformat()
        
        self.data["users"][user_id] = user_data
        self._save_data()
        return user_data
    
    def get_user(self, user_id: str) -> Dict[str, Any] | None:
        """Busca um usuário pelo ID"""
        return self.data["users"].get(user_id)
    
    def get_user_by_email(self, email: str) -> Dict[str, Any] | None:
        """Busca um usuário pelo email"""
        for user in self.data["users"].values():
            if user.get("email") == email:
                return user
        return None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Retorna todos os usuários"""
        return list(self.data["users"].values())
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any] | None:
        """Atualiza um usuário existente"""
        if user_id not in self.data["users"]:
            return None
        
        user = self.data["users"][user_id]
        user.update(update_data)
        user['updated_at'] = datetime.now().isoformat()
        
        self.data["users"][user_id] = user
        self._save_data()
        return user
    
    # Métodos para Donations
    def create_donation(self, donation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova doação"""
        donation_id = self.generate_id()
        donation_data['id'] = donation_id
        donation_data['created_at'] = datetime.now().isoformat()
        donation_data['updated_at'] = datetime.now().isoformat()
        
        self.data["donations"][donation_id] = donation_data
        self._save_data()
        return donation_data
    
    def get_donation(self, donation_id: str) -> Dict[str, Any] | None:
        """Busca uma doação pelo ID"""
        return self.data["donations"].get(donation_id)
    
    def get_all_donations(self) -> List[Dict[str, Any]]:
        """Retorna todas as doações"""
        return list(self.data["donations"].values())
    
    def update_donation(self, donation_id: str, update_data: Dict[str, Any]) -> Dict[str, Any] | None:
        """Atualiza uma doação existente"""
        if donation_id not in self.data["donations"]:
            return None
        
        donation = self.data["donations"][donation_id]
        donation.update(update_data)
        donation['updated_at'] = datetime.now().isoformat()
        
        self.data["donations"][donation_id] = donation
        self._save_data()
        return donation

# Instância global do banco de dados
db = LocalDatabase()

def initialize_database():
    """Inicializa o banco de dados"""
    global db
    db = LocalDatabase()
    print("Banco de dados local inicializado!")

def get_database():
    """Retorna a instância do banco de dados"""
    return db