from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas


def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(title=data.title, description=data.description, status="pending")
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session, status: Optional[str] = None) -> List[models.Task]:
    q = db.query(models.Task)
    if status:
        q = q.filter(models.Task.status == status)
    return q.order_by(models.Task.created_at.desc()).all()


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task_id: int, data: schemas.TaskUpdate) -> Optional[models.Task]:
    task = get_task(db, task_id)
    if not task:
        return None
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.status is not None:
        task.status = data.status
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int) -> bool:
    task = get_task(db, task_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True


