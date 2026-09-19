from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./data/learning.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Learner(Base):
    __tablename__ = "learners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    learner_id = Column(Integer, index=True)
    item_id = Column(String, index=True)
    topic_id = Column(String, index=True)

    interaction_type = Column(String)

    score = Column(Float, nullable=True)
    time_to_answer = Column(Float, nullable=True)

    watch_percentage = Column(Float, nullable=True)
    pause_count = Column(Integer, default=0)
    rewatch_count = Column(Integer, default=0)

    completed = Column(Boolean, default=False)

    timestamp = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
