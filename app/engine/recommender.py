import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.engine.knowledge_graph import (
    is_unlocked
)

from app.engine.learner_model import (
    get_learner_state
)

from app.engine.difficulty import (
    recommend_difficulty
)


ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "data" / "content.json", "r") as f:
    CONTENT = json.load(f)


def recommend_items(
    db: Session,
    learner_id: int,
    limit: int = 5
):

    state = get_learner_state(
        db,
        learner_id
    )

    mastery = state["mastery"]
    weakness = state["weakness"]

    recommendations = []

    for item in CONTENT["items"]:

        topic_id = item["topic_id"]

        topic_mastery = mastery.get(
            topic_id,
            0
        )

        # Don't expose advanced content
        # if prerequisites are not satisfied.
        if not is_unlocked(
            topic_id,
            mastery
        ):
            continue

        target_difficulty = recommend_difficulty(
            topic_mastery,
            item["difficulty"]
        )

        difficulty_distance = abs(
            item["difficulty"] - target_difficulty
        )

        difficulty_score = max(
            0,
            1 - difficulty_distance / 4
        )

        weakness_score = weakness.get(
            topic_id,
            1.0
        )

        mastery_gap = 1 - topic_mastery

        # Prefer learning items for weak topics.
        score = (
            weakness_score * 0.40
            + mastery_gap * 0.25
            + difficulty_score * 0.20
            + 0.15
        )

        if topic_mastery < 0.5:
            reason = (
                "Recommended because this topic "
                "is currently a weakness."
            )

        elif topic_mastery < 0.7:
            reason = (
                "Recommended to strengthen "
                "partial mastery."
            )

        else:
            reason = (
                "Recommended as the next "
                "appropriately difficult item."
            )

        recommendations.append({
            "item_id": item["id"],
            "topic_id": topic_id,
            "title": item["title"],
            "item_type": item["type"],
            "difficulty": item["difficulty"],
            "score": round(score, 4),
            "reason": reason
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:limit]
