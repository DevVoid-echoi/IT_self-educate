def lib_evaluator(password: str) -> tuple[str, list[str]]:
    try:
        from zxcvbn import zxcvbn
    except:
        return "Error", ["zxcvbn library is not installed. Please install it using 'pip install zxcvbn'."]

    result = zxcvbn(password)
    score = result['score']

    strength_map = {
        0: "Weak (Easily cracked)",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong"
    }

    feedback = []
    warning = result['feedback']['warning']
    suggestions = result['feedback']['suggestions']

    if warning:
        feedback.append(f"{warning}")
    feedback.extend(suggestions)

    return strength_map[score], feedback
