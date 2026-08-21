import os
import json
import hashlib
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "auth", "user.json")

from config import ADMIN_PASSWORD

def _load_users():
    """Đọc danh sách tài khoản từ file JSON"""
    if not os.path.exists(USERS_FILE):
        return{}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_users(users):
    """Lưu danh sách tài khoản và file json"""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def _hash_password(password:str)->str:
    """Băm mật khẩu bằng SHA-256 kèm salt cố định"""
    salt = "tcp_chat_room_salt_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

def verify_password(stored_hash:str, provided_password: str)->bool:
    """So sánh mật khẩu người dùng với hash đã lưu"""
    return stored_hash == _hash_password(provided_password)

def register(username, password, role="user"):
    """Đăng ký tài khoản mới"""
    username = username.strip().lower()
    users = _load_users()

    if username in users:
        print(f"[AUTH LOG] Register failed: User '{username}' already exists.")
        return False, "User already exists"

    users[username] = {
        "password_hash": _hash_password(password),
        "role": role
    }

    _save_users(users)
    print(f"[AUTH LOG] Register success: User '{username}' registered with role '{role}'.")
    return True, "Registration successful"

def login(username, password):
    """Đăng nhập và khởi tạo Session thông tin"""
    username = username.strip().lower()
    users = _load_users()

    # Tạo admin mặc định nếu hệ thống chưa có tài khoản nào
    if not users and username == "admin":
        register("admin", ADMIN_PASSWORD, role="admin")
        users = _load_users()

    if username not in users:
        print(f"[AUTH LOG] Login failed: Username '{username}' not found.")
        return False, None

    user_data = users[username]
    if verify_password(user_data["password_hash"], password):
        # Tạo Session object trả về khi thành công
        session = {
            "username": username,
            "role": user_data.get("role", "user"),
            "authentication": True
        }
        print(f"[AUTH LOG] Login success: User '{username}' logged in successfully.")
        return True, session
    else:
        print(f"[AUTH LOG] Login failed: Invalid password for user '{username}'.")
        return False, None