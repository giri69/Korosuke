from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)  # Corresponds to name
    description = Column(String, nullable=False)  # Corresponds to description
    created_at = Column(DateTime, nullable=False)  # Corresponds to created_at
    modified_at = Column(DateTime, nullable=True)  # Corresponds to modified_date

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Required field
    user = relationship("User", back_populates="projects")  # Ensure this matches User's relationship

    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}')"
