def test_mastery_is_between_zero_and_one():

    mastery = {
        "python": 0.75,
        "loops": 0.4
    }

    for value in mastery.values():
        assert 0 <= value <= 1


def test_weakness_is_inverse_of_mastery():

    mastery = 0.8

    weakness = 1 - mastery

    assert weakness == 0.2
