import random, string

def generate_password(length: int, include_nums: bool=False, include_syms: bool=False) -> tuple[str, str]:
    """Sinh mật khẩu ngẫu nhiên và trả về tuple: (mật khẩu, độ mạnh)."""
    if length <= 0:
        raise ValueError("Length must be greater than 0")
        
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    dig = string.digits
    punct = string.punctuation
    letters = lower + upper

    ranDig = random.randint(1, max(1, length-1)) if include_nums else 0
    ranPunct = random.randint(1,max(1,length-ranDig-1)) if include_syms else 0
    remaining = length - ranDig - ranPunct


    pwd_chars = []
    # Thêm số
    for _ in range(ranDig):
        pwd_chars.append(random.choice(dig))
    # Thêm ký tự đặc biệt
    for _ in range(ranPunct):
        pwd_chars.append(random.choice(punct))
    # Thêm chữ cái thường cho số lượng còn lại
    for _ in range(remaining):
        pwd_chars.append(random.choice(letters))

    random.shuffle(pwd_chars)
    return ''.join(pwd_chars)