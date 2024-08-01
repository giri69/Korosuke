from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str  
    description: Optional[str] = None  # Optional field
    user_id: int  # Required field

# Schema for creating a project
class ProjectCreate(ProjectBase):
    pass

# Schema for updating a project
class ProjectUpdate(ProjectBase):
    modified_at: Optional[datetime] = None  # Optional field

# Schema for reading (response) a project
class ProjectResponse(BaseModel):
    id: int  # Required field
    name: str  # Required field
    description: Optional[str] = None  # Optional field
    created_at: datetime  # Required field
    modified_date: Optional[datetime] = None  # Optional field
    user_id: int  # Required field

    class Config:
        orm_mode = True  # Allows reading data from ORM objects
