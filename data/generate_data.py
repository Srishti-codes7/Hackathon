import json
import random
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import (
    init_db,
    SessionLocal,
    Learner,
    Interaction
)


ROOT = Path(__file__).resolve().parents[1]

with open(ROOT / "data" / "content.json", "r") as f:
    content = json.load(f)


def generate():
    init_db()

    db = SessionLocal()

    try:
        db.query(Interaction).delete()
        db.query(Learner).delete()

        learners = []

        for i in range(1, 21):
            learner = Learner(
                name=f"Learner {i}"
            )

            db.add(learner)
            db.flush()

            learners.append(learner)

        for learner in learners:

            # Each learner gets a different baseline ability.
            ability = random.uniform(0.45, 0.95)

            for item in content["items"]:

                # Randomly decide whether learner attempted item.
                if random.random() > 0.65:
                    continue

                topic = item["topic_id"]
                difficulty = item["difficulty"]

                base_score = (
                    ability * 100
                    - difficulty * random.uniform(3, 10)
                    + random.gauss(0, 8)
                )

                score = max(
                    0,
                    min(100, base_score)
                )

                completed = score >= 50

                interaction = Interaction(
                    learner_id=learner.id,
                    item_id=item["id"],
                    topic_id=topic,
                    interaction_type=item["type"],
                    score=score if item["type"] == "quiz" else None,
                    time_to_answer=random.uniform(20, 180),
                    watch_percentage=(
                        random.uniform(60, 100)
                        if item["type"] == "video"
                        else None
                    ),
                    pause_count=random.randint(0, 3),
                    rewatch_count=random.randint(0, 2),
                    completed=completed
                )

                db.add(interaction)

        db.commit()

        print("Generated synthetic learning data.")

    finally:
        db.close()


if __name__ == "__main__":
    generate()