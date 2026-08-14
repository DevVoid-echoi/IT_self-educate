import string

COMMON_WORDS = {
    "password", "qwerty", "password1", "111111", "iloveyou", "admin",
    "welcome", "monkey", "login", "letmein", "football", "starwars",
    "dragon", "passw0rd", "master", "hello", "freedom"
}

def check_common_sequences(password: str) -> bool:
    """Check if the password contains common sequences."""
    pwd_split = list(password.lower())
    for i in range(len(pwd_split)-2):
        cond1 = ord(pwd_split[i]) == ord(pwd_split[i+1])-1 
        cond2 = ord(pwd_split[i+1]) == ord(pwd_split[i+2])-1
        if cond1 and cond2:
            return True
    return False

def manual_evaluator(password: str) -> tuple [str,list[str]]:
    """Evaluate the strength of the password."""
    score = 0
    feedback = []

    length = len(password)
    has_num = any(c.isdigit() for c in password)
    has_sym = any(c in string.punctuation for c in password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)

    if length >= 20:
        score += 15
    elif length >= 12:
        score += 10
    elif length >= 8:
        score += 5

    if has_num: 
        score += 5
    if has_sym:
        score += 5
    if has_upper and has_lower:
        score += 5

    pwd_lower = password.lower()
    for w in COMMON_WORDS:
        if w in pwd_lower:
            score -= 10
            feedback.append(f"Contains common word: '{w}'")
            break

    if check_common_sequences(password):
        score -= 10
        feedback.append("Contains common sequence of characters.")

    if score <=5:
        strength = "Weak"
    elif score <= 10:
        strength = "Moderate"
    elif score <= 15:
        strength = "Strong"
    else: 
        strength = "Very Strong"
    
    return strength, feedback
    