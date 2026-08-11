from src.generator import generate_password

def get_user_inputs() -> tuple[int, bool, bool]:
    """Get user inputs for password generation."""
    while True: 
        try: 
            length = int(input("Enter the length of the password: "))
            if length <= 0:
                print("Length must be greater than 0. \n")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for length. \n")

    num = input("Do you want to include numbers in the password? (y/n): ").strip().lower()
    include_nums = (num == 'y')

    sym = input("Do you want to include symbols in the password? (y/n): ").strip().lower()
    include_syms = (sym == 'y')

    return length, include_nums, include_syms

def run_cli():
    """Run the command-line interface for password generation."""
    print("=" * 40)
    print("   CHƯƠNG TRÌNH TẠO MẬT KHẨU BẢO MẬT   ")
    print("=" * 40)
    length, include_nums, include_syms = get_user_inputs()
    password, strength = generate_password(length, include_nums, include_syms)

    print("\n" + "-" * 30)
    print(f"🔑 Mật khẩu: {password}")
    print(f"📊 Độ mạnh:  {strength}")
    print("-" * 30)