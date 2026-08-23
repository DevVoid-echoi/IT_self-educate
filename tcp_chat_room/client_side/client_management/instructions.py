import sys

def print_instructions(nickname):
    """Print instructions for users and special instructions for admin"""
    print("-" * 50)
    print(" HƯỚNG DẪN CHAT:")
    print(" - Nhập tin nhắn và bấm Enter để gửi.")
    print(" - Gõ '/quit' hoặc '/exit' để rời phòng chat.")
    if nickname == "admin":
        print(" - Gõ /kick <user_name> để đuổi người dùng khỏi phòng chat")
        print(" - Gõ /ban <user_name> để cấm người dùng vào phòng chat")
    print("-" * 50)
