from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import (
    get_db,
    Learner,
    Interaction
)

from app.schemas import (
    LearnerCreate,
    InteractionCreate
)

from app.engine.learner_model import (
    get_learner_state
)


router = APIRouter(
    prefix="/learner",
    tags=["Learners"]
)


@router.post("/")
def create_learner(
    data: LearnerCreate,
    db: Session = Depends(get_db)
):

    learner = Learner(
        name=data.name
    )

    db.add(learner)
    db.commit()
    db.refresh(learner)

    return {
        "id": learner.id,
        "name": learner.name
    }


@router.get("/{learner_id}/state")
def learner_state(
    learner_id: int,
    db: Session = Depends(get_db)
):

    learner = (
        db.query(Learner)
        .filter(
            Learner.id == learner_id
        )
        .first()
    )

    if not learner:
        raise HTTPException(
            status_code=404,
            detail="Learner not found"
        )

    return get_learner_state(
        db,
        learner_id
    )


@router.post("/interaction")
def record_interaction(
    data: InteractionCreate,
    db: Session = Depends(get_db)
):

    learner = (
        db.query(Learner)
        .filter(
            Learner.id == data.learner_id
        )
        .first()
    )

    if not learner:
        raise HTTPException(
            status_code=404,
            detail="Learner not found"
        )

    interaction = Interaction(
        learner_id=data.learner_id,
        item_id=data.item_id,
        topic_id=data.topic_id,
        interaction_type=data.interaction_type,
        score=data.score,
        time_to_answer=data.time_to_answer,
        watch_percentage=data.watch_percentage,
        pause_count=data.pause_count,
        rewatch_count=data.rewatch_count,
        completed=data.completed
    )

    db.add(interaction)
    db.commit()

    return {
        "message": "Interaction recorded",
        "interaction_id": interaction.id
    }
