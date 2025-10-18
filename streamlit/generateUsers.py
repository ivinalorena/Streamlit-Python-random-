import json
import hashlib
import secrets
import time
from pathlib import Path

def hash_password(password):
    """Gera hash seguro da senha"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    current_dir = Path(__file__).parent
    json_path = current_dir / "users_hashed.json"
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["USERS"]
    except FileNotFoundError:
        # Criar usuários padrão se não existir
        default_users = {
            "admin": hash_password("admin123"),
            "user1": hash_password("password123")
        }
        save_users(default_users)
        return default_users
    except Exception as e:
        print(f"Erro ao carregar usuários: {e}")
        return {}

def save_users(users_dict):
    """Salva usuários com hash no JSON"""
    current_dir = Path(__file__).parent
    json_path = current_dir / "users_hashed.json"
    
    data = {"USERS": users_dict}
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def validate_user(username, password):
    """Validação segura com proteção contra timing attacks"""
    users = load_users()
    # Sempre fazer hash da senha fornecida
    password_hash = hash_password(password)
    
    # Proteção contra timing attacks
    time.sleep(0.1)  # Delay constante
    
    if username in users:
        stored_hash = users[username]
        # Comparação segura
        return secrets.compare_digest(password_hash, stored_hash)
    
    return False

def add_user(username, password):
    """Adiciona novo usuário com hash"""
    users = load_users()
    users[username] = hash_password(password)
    save_users(users)
    return True

# Carregar usuários na inicialização
USERS = load_users()