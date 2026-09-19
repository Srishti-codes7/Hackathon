from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.engine.recommender import recommend_items


router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)


@router.get("/{learner_id}")
def get_recommendations(
    learner_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):

    return {
        "learner_id": learner_id,
        "recommendations": recommend_items(
            db,
            learner_id,
            limit
        )
    }
