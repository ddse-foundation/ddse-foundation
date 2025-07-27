from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database, auth
from typing import List

router = APIRouter(prefix="/teams", tags=["teams"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

get_current_user = auth.get_current_user

@router.post("/", response_model=schemas.TeamOut)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Create a new team following IDR-001 API conventions"""
    # Check if team name already exists
    existing_team = db.query(models.Team).filter(models.Team.name == team.name).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="Team name already exists")

    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    # Assign current user to the team they created
    current_user.team_id = db_team.id
    db.commit()

    return db_team

@router.get("/", response_model=List[schemas.TeamOut])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all teams - public endpoint for team discovery"""
    return db.query(models.Team).offset(skip).limit(limit).all()

@router.get("/{team_id}", response_model=schemas.TeamOut)
def read_team(team_id: int, db: Session = Depends(get_db)):
    """Get specific team details"""
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.post("/{team_id}/join")
def join_team(team_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Allow user to join an existing team"""
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")

    current_user.team_id = team_id
    db.commit()
    return {"message": f"Successfully joined team {db_team.name}"}
