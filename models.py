from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Project(Base):
    __tablename__="projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)

    places=relationship(
        "ProjectPlace",
        back_populates="project",
        cascade="all, delete"

    )

class ProjectPlace(Base):
    __tablename__ = "project_places"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))

    external_id = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    visited = Column(Boolean, default=False)

    project = relationship("Project", back_populates="places")
