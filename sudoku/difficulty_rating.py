def calculate_difficulty(summary):
    techniques = summary["techniques"]
    naked_singles = techniques["naked_single"]
    hidden_singles = techniques["hidden_single"]
    naked_pairs = techniques["naked_pair"]
    score = 0
    score += naked_singles * 1
    score += hidden_singles * 3
    score += naked_pairs * 5
    return score
def get_difficulty_level(score):
    if score <= 10:
        return "Easy"
    elif score <= 25:
        return "Medium"
    else:
        return "Hard"
def rate_solver(summary):
    score = calculate_difficulty(summary)
    level = get_difficulty_level(score)
    return {
        "score": score,
        "level": level}