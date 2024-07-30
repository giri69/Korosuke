from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Assuming String is appropriate
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))  # Correct foreign key format

    owner = relationship("User", back_populates="projects")  # Relationship configuration
