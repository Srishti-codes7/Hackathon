from app.engine.difficulty import (
    recommend_difficulty
)


def test_high_mastery_increases_difficulty():

    result = recommend_difficulty(
        mastery=0.9,
        current_difficulty=2
    )

    assert result == 3


def test_low_mastery_decreases_difficulty():

    result = recommend_difficulty(
        mastery=0.3,
        current_difficulty=3
    )

    assert result == 2


def test_medium_mastery_keeps_difficulty():

    result = recommend_difficulty(
        mastery=0.65,
        current_difficulty=2
    )

    assert result == 2
