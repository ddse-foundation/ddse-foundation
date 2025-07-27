from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database, auth
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for current user
get_current_user = auth.get_current_user

@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Create a new task following IDR-001 API conventions and IDR-002 validation patterns"""
    if not current_user.team_id:
        raise HTTPException(status_code=400, detail="User must be assigned to a team to create tasks")

    db_task = models.Task(**task.dict(), owner_id=current_user.id, team_id=current_user.team_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[schemas.TaskOut])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Get tasks for current user's team following team-based access control from EDR-001"""
    if not current_user.team_id:
        return []
    return db.query(models.Task).filter(models.Task.team_id == current_user.team_id).offset(skip).limit(limit).all()

@router.get("/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Get specific task with team-based access control"""
    if not current_user.team_id:
        raise HTTPException(status_code=403, detail="User must be assigned to a team")

    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.team_id == current_user.team_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Update task following IDR-002 validation and team access control"""
    if not current_user.team_id:
        raise HTTPException(status_code=403, detail="User must be assigned to a team")

    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.team_id == current_user.team_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Apply updates only for non-None values per IDR-002
    for var, value in vars(task).items():
        if value is not None:
            setattr(db_task, var, value)

    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Delete task with proper team access control"""
    if not current_user.team_id:
        raise HTTPException(status_code=403, detail="User must be assigned to a team")

    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.team_id == current_user.team_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return None
