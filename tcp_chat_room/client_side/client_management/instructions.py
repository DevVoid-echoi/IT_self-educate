import sys
from server_side.client_management.actions import user_sessions
from auth.rbac import has_permission, Permission

def print_instructions(nickname, user_role = "user"):
    """Print instructions for users and special instructions for admin"""
    print("-" * 50)
    print(" HƯỚNG DẪN CHAT:")
    print(" - Nhập tin nhắn và bấm Enter để gửi.")
    print(" - Gõ '/quit' hoặc '/exit' để rời phòng chat.")
    if has_permission(user_role, Permission.KICK):
        print(" - Gõ /kick <user_name> để đuổi người dùng khỏi phòng chat")
    if has_permission(user_role, Permission.BAN):
        print(" - Gõ /ban <user_name> để cấm người dùng vào phòng chat")
    print("-" * 50)
