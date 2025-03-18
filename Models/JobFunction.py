from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Date, UniqueConstraint
from Models.Connection import Base
from sqlalchemy.orm import relationship
from Models.AssessmentRole import AssessmentRole
from Models.JobLevel import JobLevel

class JobFunction(Base):
    __tablename__ = 'job_functions'

    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String(12), nullable=False)
    label = Column(String(180), nullable=False)
    level_id = Column(Integer, ForeignKey('job_level.id'), nullable=False)
    definisi = Column(String(255))

    # Relationship with Job Level
    level = relationship("JobLevel", back_populates="job_functions")

    # Relationship with Assessment Role
    roles = relationship("AssessmentRole", back_populates="function")