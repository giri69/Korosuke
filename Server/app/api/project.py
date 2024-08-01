from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


from app.db.base import get_db  
from app.crud.project import create_project, update_project, get_project  # Import CRUD functions
from app.models.Project import Project  # Import your SQLAlchemy Project model
from app.crud.project import get_projects_by_user_id

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_project(project_data: dict, db: Session = Depends(get_db)):
    try:
        # Create the project and get the SQLAlchemy model instance
        created_project = create_project(db=db, data=project_data)

        print("Created Project:", created_project)

        # Return the created project as a dictionary
        return {
            "id": created_project.id,
            "name": created_project.name,
            "description": created_project.description,
            "created_at": created_project.created_at,
            "modified_date": created_project.modified_at,
            "user_id": created_project.user_id
        }
    except HTTPException as e:
        print(e)
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while creating the project")


@router.put("/{project_id}")
def update_existing_project(project_id: int, project_data: dict, db: Session = Depends(get_db)):
    try:
        updated_project = update_project(db=db, project_id=project_id, data=project_data)
        
        return {
            "id": updated_project.id,
            "name": updated_project.name,
            "description": updated_project.description,
            "created_at": updated_project.created_at,
            "modified_date": updated_project.modified_at,
            "user_id": updated_project.user_id
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while updating the project")

@router.get("/{project_id}")
def read_project(project_id: int, db: Session = Depends(get_db)):
    try:
        project = get_project(db=db, project_id=project_id)
        
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "modified_date": project.modified_at,
            "user_id": project.user_id
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the project")

@router.get("/user/{user_id}", response_model=List[dict])
def get_projects_for_user(user_id: int, db: Session = Depends(get_db)):
    try:
        projects = get_projects_by_user_id(db=db, user_id=user_id)
        return [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at,
                "modified_date": project.modified_at,
                "user_id": project.user_id
            }
            for project in projects
        ]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the projects")