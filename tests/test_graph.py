from app.engine.knowledge_graph import (
    get_prerequisites,
    is_unlocked
)


def test_python_has_no_prerequisites():

    assert get_prerequisites(
        "python_basics"
    ) == []


def test_variables_requires_python():

    assert get_prerequisites(
        "variables"
    ) == ["python_basics"]


def test_topic_unlocking():

    mastery = {
        "python_basics": 0.8
    }

    assert is_unlocked(
        "variables",
        mastery
    )


def test_topic_locked():

    mastery = {
        "python_basics": 0.4
    }

    assert not is_unlocked(
        "variables",
        mastery
    )
