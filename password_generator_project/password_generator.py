import random, string

def set_value():
    global length, num, sym 

    length = int(input("Enter the length of the password: "))
    if length <= 0:
        print("Length must be greater than 0")
        exit()

    num = input("Do you want to include numbers in the password? (y/n): ").lower()
    if num == 'y':
        num = True
    else: 
        num = False

    sym = input("Do you want to include symbols in the password? (y/n): ").lower()
    if sym == 'y':
        sym = True
    else: 
        sym = False


def password(length, num=False, sym=False):
    """ length of password, number in password, and strength(weak, medium, strong, very strong)"""

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    letter = lower + upper
    dig = string.digits
    punct = string.punctuation
    pwd = ''

    global strength

    '''
    # WEAK
    if length <= 8 and (num == False or sym == False):
        ranDig = random.randint(1, max(1, length-1)) if num else 0
        ranPunct = random.randint(1,max(1,length-ranDig-1)) if sym else 0
        # 1. Thêm số
        for _ in range(ranDig):
            pwd += random.choice(dig)
        
        # 2. Thêm ký tự đặc biệt
        for _ in range(ranPunct):
            pwd += random.choice(punct)
            
        # 3. Thêm chữ cái thường cho số lượng còn lại
        remaining = length - ranDig - ranPunct
        for _ in range(remaining):
            pwd += random.choice([lower, uper])
        strength = 'Weak'

    # MEDIUM
    elif length <= 12 or (length <= 15 and (num == False or sym == False)):
        ranDig = random.randint(1, max(1, length-1)) if num else 0
        ranPunct = random.randint(1,max(1,length-ranDig-1)) if sym else 0
        # 1. Thêm số
        for _ in range(ranDig):
            pwd += random.choice(dig)
        
        # 2. Thêm ký tự đặc biệt
        for _ in range(ranPunct):
            pwd += random.choice(punct)
            
        # 3. Thêm chữ cái thường cho số lượng còn lại
        remaining = length - ranDig - ranPunct
        for _ in range(remaining):
            pwd += random.choice(letter)
        strength = 'Medium'

    # STRONG
    elif length <= 15 or num == False or sym == False:
        ranDig = random.randint(1, max(1, length-1)) if num else 0
        ranPunct = random.randint(1,max(1,length-ranDig-1)) if sym else 0
        # 1. Thêm số
        for _ in range(ranDig):
            pwd += random.choice(dig)
        
        # 2. Thêm ký tự đặc biệt
        for _ in range(ranPunct):
            pwd += random.choice(punct)
            
        # 3. Thêm chữ cái thường cho số lượng còn lại
        remaining = length - ranDig - ranPunct
        for _ in range(remaining):
            pwd += random.choice(letter)
        strength = 'Strong'
        
    # VERY STRONG
    else:
        ranDig = random.randint(1, max(1, length-1)) if num else 0
        ranPunct = random.randint(1,max(1,length-ranDig-1)) if sym else 0
        # 1. Thêm số
        for _ in range(ranDig):
            pwd += random.choice(dig)
        
        # 2. Thêm ký tự đặc biệt
        for _ in range(ranPunct):
            pwd += random.choice(punct)
            
        # 3. Thêm chữ cái thường cho số lượng còn lại
        remaining = length - ranDig - ranPunct
        for _ in range(remaining):
            pwd += random.choice(letter)
        strength = 'Very strong'
    '''

    # Phân loại độ mạnh
    if length <= 8 and (num == False or sym == False):
        strength = 'Weak'
    elif length <= 12 or (length <= 15 and (num == False or sym == False)):
        strength = 'Medium'
    elif length <= 15 or num == False or sym == False:
        strength = 'Strong'
    else:
        strength = 'Very strong'

    # Sinh độ dài ngẫu nhiên của số và ký tự đặc biệt
    ranDig = random.randint(1, max(1, length-1)) if num else 0
    ranPunct = random.randint(1,max(1,length-ranDig-1)) if sym else 0

    # Thêm số
    for _ in range(ranDig):
        pwd += random.choice(dig)
        
    # Thêm ký tự đặc biệt
    for _ in range(ranPunct):
        pwd += random.choice(punct)
            
    # Thêm chữ cái thường cho số lượng còn lại
    remaining = length - ranDig - ranPunct
    char_souce = lower if strength == 'weak' else letter
    for _ in range(remaining):
        pwd += random.choice(letter)
    

    # Tráo đổi vị trí ký tự
    pwd = list(pwd)
    random.shuffle(pwd)
    return ''.join(pwd)


def generate_password():
    set_value()
    print("Password: ", password(length, num, sym))
    print("Strength: ", strength)

generate_password()