from pydantic import BaseModel, constr
from typing import Optional, List
import datetime

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=32)

class UserCreate(UserBase):
    password: constr(min_length=6)
    team_id: Optional[int] = None

class UserOut(UserBase):
    id: int
    is_active: bool
    team_id: Optional[int]
    class Config:
        from_attributes = True

class TeamBase(BaseModel):
    name: constr(min_length=2, max_length=32)

class TeamCreate(TeamBase):
    pass

class TeamOut(TeamBase):
    id: int
    members: List[UserOut] = []
    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=128)
    description: Optional[str] = None
    status: Optional[str] = "todo"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=128)] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskOut(TaskBase):
    id: int
    owner_id: int
    team_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Response models for standardized API responses per EDR-002
class ErrorResponse(BaseModel):
    detail: str
    type: str
    path: str

class ValidationErrorResponse(ErrorResponse):
    errors: List[dict]

class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None
