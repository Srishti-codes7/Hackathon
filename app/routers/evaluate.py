from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.engine.evaluation import evaluate_system


router = APIRouter(
    prefix="/evaluate",
    tags=["Evaluation"]
)


@router.get("")
def evaluate(
    db: Session = Depends(get_db)
):

    return evaluate_system(db)
