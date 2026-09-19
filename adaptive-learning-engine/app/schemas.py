from typing import Optional, Dict, List

from pydantic import BaseModel, Field


class InteractionCreate(BaseModel):
    learner_id: int
    item_id: str
    topic_id: str

    interaction_type: str

    score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )

    time_to_answer: Optional[float] = Field(
        default=None,
        ge=0
    )

    watch_percentage: Optional[float] = Field(
        default=None,
        ge=0,
        le=100
    )

    pause_count: int = Field(default=0, ge=0)

    rewatch_count: int = Field(default=0, ge=0)

    completed: bool = False


class LearnerCreate(BaseModel):
    name: str


class TopicState(BaseModel):
    topic_id: str
    mastery: float
    engagement: float
    weakness: float


class LearnerState(BaseModel):
    learner_id: int
    topics: List[TopicState]


class Recommendation(BaseModel):
    item_id: str
    topic_id: str
    title: str
    item_type: str
    difficulty: int
    score: float
    reason: str


class EvaluationResult(BaseModel):
    completion_rate: float
    average_mastery: float
    engagement_rate: float
    learners_evaluated: int
