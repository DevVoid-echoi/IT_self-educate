import argparse
import string
from src.generator import generate_password
from src.evaluator import evaluate_strength

def arg_parser() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Password Generator & Strength Evaluator Tool")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate a random password")
    parser.add_argument("-e", "--evaluate", type=str, metavar="PASSWORD", const="", nargs="?", help="Evaluate an existing password")

    return parser.parse_args()

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

def run_generator_mode():
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

def run_evaluator_mode(password: str):
    "Run the command-line interface for password evaluation."
    print("=" * 40)
    print("   CHƯƠNG TRÌNH ĐÁNH GIÁ MẬT KHẨU   ")
    print("=" * 40)

    if not password:
        password = input("Nhập mật khẩu cần kiểm tra: ").strip()

    length = len(password)
    include_nums = any(char.isdigit() for char in password)
    include_syms = any(char in string.punctuation for char in password)
    
    strength = evaluate_strength(length, include_nums, include_syms)

    print("\n" + "-" * 30)
    print(f"🔑 Mật khẩu: {password}")
    print(f"📊 Độ mạnh:  {strength}")
    print("-" * 30)

def run_cli():
    "Run the command-line interface for password generation and evaluation."
    args = arg_parser()

    if args.evaluate is not None:
        run_evaluator_mode(args.evaluate)
    else:
        run_generator_mode()