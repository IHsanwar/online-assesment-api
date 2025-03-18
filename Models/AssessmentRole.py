from Models.Connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Date, UniqueConstraint
from sqlalchemy.orm import relationship


class AssessmentRole(Base):
    __tablename__ = 'assessment_role'

    id = Column(Integer, primary_key=True, nullable=False)
    model = Column(Enum('keybe', 'definisi'), nullable=False)
    function_id = Column(Integer, ForeignKey('job_functions.id'), nullable=False)
    label = Column(String)

    # Relationship with Job Functions
    function = relationship("JobFunction", back_populates="roles")

    # Relationship with Indicators
    indicators = relationship("Indicator", back_populates="role")