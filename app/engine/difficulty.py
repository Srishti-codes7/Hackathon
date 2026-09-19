def recommend_difficulty(
    mastery: float,
    current_difficulty: int
):

    # Very strong performance:
    # increase challenge.
    if mastery >= 0.85:
        return min(
            current_difficulty + 1,
            5
        )

    # Weak performance:
    # reduce difficulty.
    if mastery < 0.5:
        return max(
            current_difficulty - 1,
            1
        )

    return current_difficulty