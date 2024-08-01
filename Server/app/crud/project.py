from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from app.models.Project import Project
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from datetime import datetime, timezone


def create_project(db: Session, data: dict):
    try:
        print("Level 1: Starting project creation")
        
        # Set created_at to the current UTC time
        data['created_at'] = datetime.now(timezone.utc)

        # Set default user_id to 6 if user_id is not provided or is 0
        if 'user_id' not in data or data['user_id'] == 0:
            data['user_id'] = 6
        
        project = Project(**data)
        print("Level 2: Project instance created:", project)
        db.add(project)
        print("Level 3: Project added to session")
        db.commit()
        print("Level 4: Session committed")
        db.refresh(project)
        print("Level 5: Project refreshed from database")
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
        db.commit()
        return project
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the project")

def get_project(db: Session, project_id: int):
    project = db.query(Project).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID {project_id} not found")
    return project
