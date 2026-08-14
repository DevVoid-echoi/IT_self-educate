import random, string

def generate_password(length: int, 
include_nums: bool=False, 
include_syms: bool=False,
include_lower: bool = False,
include_upper: bool = False) -> str:
    """Sinh mật khẩu ngẫu nhiên."""
    if length <= 0:
        raise ValueError("Length must be greater than 0!")
        
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    dig = string.digits
    punct = string.punctuation
    if not any([include_lower, include_upper, include_nums, include_syms]):
        raise ValueError("Please choose at least one character type!")

    pwd_chars = []
    pool = ""

    if include_lower:
        pwd_chars.append(random.choice(lower))
        pool += lower
    if include_upper:
        pwd_chars.append(random.choice(upper))
        pool += upper
    if include_nums:
        pwd_chars.append(random.choice(dig))
        pool += dig
    if include_syms:
        pwd_chars.append(random.choice(punct))
        pool += punct

    if len(pwd_chars) > length:
        raise ValueError(f"Password length ({length}) is too short for all requirements ({len(pwd_chars)}")

    remaining = length - len(pwd_chars)
    
    for _ in range(remaining):
        pwd_chars.append(random.choice(pool))

    random.shuffle(pwd_chars)
    
    return ''.join(pwd_chars)