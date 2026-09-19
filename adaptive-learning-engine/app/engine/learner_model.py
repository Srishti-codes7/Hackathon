from collections import defaultdict

from sqlalchemy.orm import Session

from app.database import Interaction


def calculate_mastery(
    db: Session,
    learner_id: int
):

    interactions = (
        db.query(Interaction)
        .filter(
            Interaction.learner_id == learner_id
        )
        .all()
    )

    scores = defaultdict(list)

    for interaction in interactions:

        if interaction.score is not None:
            scores[interaction.topic_id].append(
                interaction.score / 100
            )

    mastery = {}

    for topic_id, values in scores.items():

        # Give more importance to recent performance
        if len(values) == 1:
            mastery[topic_id] = values[0]

        else:
            weighted = 0
            weight_sum = 0

            for i, value in enumerate(values):
                weight = i + 1
                weighted += value * weight
                weight_sum += weight

            mastery[topic_id] = weighted / weight_sum

    return mastery


def calculate_engagement(
    db: Session,
    learner_id: int
):

    interactions = (
        db.query(Interaction)
        .filter(
            Interaction.learner_id == learner_id
        )
        .all()
    )

    if not interactions:
        return 0.0

    engagement_scores = []

    for interaction in interactions:

        score = 0.0

        if interaction.completed:
            score += 0.4

        if interaction.watch_percentage:
            score += (
                interaction.watch_percentage / 100
            ) * 0.3

        # Excessive pauses indicate friction.
        pause_penalty = min(
            interaction.pause_count * 0.05,
            0.2
        )

        score += 0.2
        score -= pause_penalty

        # Rewatching can indicate either interest
        # or difficulty. We treat moderate rewatching
        # as positive engagement.
        if interaction.rewatch_count > 0:
            score += min(
                interaction.rewatch_count * 0.05,
                0.1
            )

        engagement_scores.append(
            max(0, min(1, score))
        )

    return sum(engagement_scores) / len(
        engagement_scores
    )


def calculate_weakness(
    mastery: dict
):

    return {
        topic_id: 1 - value
        for topic_id, value in mastery.items()
    }


def get_learner_state(
    db: Session,
    learner_id: int
):

    mastery = calculate_mastery(
        db,
        learner_id
    )

    engagement = calculate_engagement(
        db,
        learner_id
    )

    weakness = calculate_weakness(
        mastery
    )

    return {
        "mastery": mastery,
        "engagement": engagement,
        "weakness": weakness
    }
