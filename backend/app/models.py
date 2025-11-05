from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime
from .db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=True)
    status = Column(String(32), nullable=False, default="pending", index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))


