from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import get_db, Base, engine
from .. import crud, schemas, models


Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/", response_model=schemas.TaskOut, status_code=201)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, data)


@router.get("/", response_model=List[schemas.TaskOut])
def list_all(status: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    return crud.list_tasks(db, status=status)


@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_one(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_one(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
def delete_one(task_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_task(db, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


