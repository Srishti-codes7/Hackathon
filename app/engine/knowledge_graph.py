import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "data" / "content.json", "r") as f:
    CONTENT = json.load(f)


TOPICS = {
    topic["id"]: topic
    for topic in CONTENT["topics"]
}


def get_prerequisites(topic_id: str):
    topic = TOPICS.get(topic_id)

    if not topic:
        return []

    return topic.get("prerequisites", [])


def is_unlocked(topic_id: str, mastery: dict, threshold: float = 0.7):
    prerequisites = get_prerequisites(topic_id)

    if not prerequisites:
        return True

    return all(
        mastery.get(prerequisite, 0) >= threshold
        for prerequisite in prerequisites
    )


def get_unlocked_topics(mastery: dict):
    return [
        topic_id
        for topic_id in TOPICS
        if is_unlocked(topic_id, mastery)
    ]


def get_topic_depth(topic_id: str):
    prerequisites = get_prerequisites(topic_id)

    if not prerequisites:
        return 0

    return 1 + max(
        get_topic_depth(p)
        for p in prerequisites
    )
