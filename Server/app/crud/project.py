from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from app.models.Project import Project
from datetime import datetime, timezone

def create_project(db: Session, data: dict):
    try:
        data['created_at'] = datetime.now(timezone.utc)
        
        if 'user_id' not in data or data['user_id'] == 0:
            data['user_id'] = 6
        
        project = Project(**data)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    except IntegrityError as ie:
        db.rollback()
        print("Level 2.1: Integrity error occurred", str(ie))
        raise HTTPException(status_code=400, detail="Integrity error: " + str(ie))
    except SQLAlchemyError as e:
        db.rollback()
        print("Level 2.2: SQLAlchemy error occurred", str(e))
        raise HTTPException(status_code=500, detail="An error occurred while creating the project")
    except Exception as e:
        db.rollback()
        print("Level 2.3: General error occurred", str(e))
        raise HTTPException(status_code=500, detail="An unknown error occurred while creating the project")

def update_project(db: Session, project_id: int, data: dict):
    try:
        project = db.query(Project).filter_by(id=project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
        
        for key, value in data.items():
            setattr(project, key, value)
        
        # Update the modified_at field to the current UTC time
        project.modified_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(project)
        return project
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the project")
    
def get_project(db: Session, project_id: int):
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
    return project

def get_projects_by_user_id(db: Session, user_id: int):
    return db.query(Project).filter(Project.user_id == user_id).all()
