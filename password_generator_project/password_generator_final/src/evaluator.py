def evaluate_strength(length: int, include_nums: bool, include_syms: bool) -> str:
    """Evaluate the strength of the password based on length and character inclusion."""
    if length <= 8 and (not include_nums or not include_syms):
        return 'Weak'
    elif length <= 12 or (length <= 15 and (not include_nums or not include_syms)):
        return 'Medium'
    elif length <= 20 or (length <= 25 and (not include_nums or not include_syms)):
        return 'Strong'
    else:
        return 'Very Strong'