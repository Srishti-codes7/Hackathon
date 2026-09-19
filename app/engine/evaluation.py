from sqlalchemy.orm import Session

from app.database import Learner, Interaction
from app.engine.learner_model import (
    calculate_mastery,
    calculate_engagement
)


def evaluate_system(
    db: Session
):

    learners = db.query(Learner).all()

    if not learners:
        return {
            "completion_rate": 0,
            "average_mastery": 0,
            "engagement_rate": 0,
            "learners_evaluated": 0
        }

    completion_values = []
    mastery_values = []
    engagement_values = []

    for learner in learners:

        interactions = (
            db.query(Interaction)
            .filter(
                Interaction.learner_id == learner.id
            )
            .all()
        )

        if interactions:

            completed = sum(
                1
                for x in interactions
                if x.completed
            )

            completion_values.append(
                completed / len(interactions)
            )

        mastery = calculate_mastery(
            db,
            learner.id
        )

        if mastery:
            mastery_values.append(
                sum(mastery.values())
                / len(mastery)
            )

        engagement_values.append(
            calculate_engagement(
                db,
                learner.id
            )
        )

    return {
        "completion_rate": round(
            sum(completion_values)
            / max(len(completion_values), 1),
            4
        ),

        "average_mastery": round(
            sum(mastery_values)
            / max(len(mastery_values), 1),
            4
        ),

        "engagement_rate": round(
            sum(engagement_values)
            / max(len(engagement_values), 1),
            4
        ),

        "learners_evaluated": len(learners)
    }
