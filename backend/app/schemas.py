from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: str = Field(default="pending")


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[str] = Field(default=None)


class TaskOut(TaskBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


