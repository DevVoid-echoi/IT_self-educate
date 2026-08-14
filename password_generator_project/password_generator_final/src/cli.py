import argparse
import string
import sys  
from src.generator import generate_password
from src.evaluators.manual_evaluator import manual_evaluator
from src.evaluators.lib_evaluator import lib_evaluator  

def arg_parser() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Password Generator & Strength Evaluator Tool")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate a random password")

    parser.add_argument("-e", "--evaluate", type=str, metavar="PASSWORD", const="", nargs="?", help="Evaluate an existing password")
    
    parser.add_argument("-n", "--engine", 
        choices=["manual", "lib", "both"], 
        default = "both",
        help="Choose an engine to evaluate password: 'manual, 'lib', or 'both'")

    return parser.parse_args()

def get_user_inputs() -> tuple[int, bool, bool, bool, bool]:
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

    lw = input("Do you want to include lower letters in the password? (y/n): ").strip().lower()
    include_lower = (lw == 'y')

    up = input("Do you want to include upper letters in the password? (y/n): ").strip().lower()
    include_upper = (up == 'y')

    return length, include_nums, include_syms, include_lower, include_upper

def display_result (password: str, engine: str):
    """Display the result based on chosen engine"""
    print("\n" + "-" * 30)
    print(f"Password: {password}")

    if engine in ["manual", "both"]:
        manual_strength, manual_feedback = manual_evaluator(password)
        print(f"Strength (Manual): {manual_strength}")
        if manual_feedback:
            print(f"Notes: {', '.join(manual_feedback)}")
    if engine in ["lib", "both"]:
        lib_strength, lib_feedback = lib_evaluator(password)
        print(f"Strength (Library): {lib_strength}")
        if lib_feedback:
            print(f"Notes: {', '.join(lib_feedback)}")
    
    print("-" * 30)

def run_generator_mode(engine: str):
    """Run the command-line interface for password generation."""
    print("=" * 40)
    print("   Password Generator Program   ")
    print("=" * 40)

    length, include_nums, include_syms, include_lower, include_upper = get_user_inputs()
    password = generate_password(length, include_nums, include_syms, include_lower, include_upper)

    display_result(password, engine)

def run_evaluator_mode(password: str, engine: str):
    "Run the command-line interface for password evaluation."
    print("=" * 40)
    print("   Password Evaluator Program   ")
    print("=" * 40)

    if not password:
        password = input("Nhập mật khẩu cần kiểm tra: ").strip()
    
    display_result(password, engine)

def run_cli():
    "Run the command-line interface for password generation and evaluation."
    args = arg_parser()

    if args.evaluate is not None:
        run_evaluator_mode(args.evaluate, args.engine)
    else:
        run_generator_mode(args.engine)