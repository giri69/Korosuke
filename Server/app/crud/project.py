from sqlalchemy.orm import Session
from app.models.projects import Project  # Import the Project class
from app.schemas.project import ProjectCreate


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Project).offset(skip).limit(limit).all()


def create_user_project(db: Session, project: ProjectCreate, user_id: int):
    db_project = Project(owner_id=user_id, **project.dict())
    db.add(db_project)
    db.commit()
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project


def update_project(db: Session, project_id: int, project: ProjectCreate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db.query(Project).filter(Project.id == project_id).update(project.dict())
        db.commit()
    return db_project
