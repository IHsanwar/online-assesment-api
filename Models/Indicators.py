from Models.Connection import *
from Models.Connection import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Date, UniqueConstraint
from sqlalchemy.orm import relationship


class Indicator(Base):
    __tablename__ = 'indicators'

    id = Column(Integer, primary_key=True, nullable=False)
    role_id = Column(Integer, ForeignKey('assessment_role.id'), nullable=False)
    assessment_tool = Column(Integer, nullable=False)
    description = Column(Text)
    indicator_item = Column(String(255), nullable=False)

    # Relationship with Assessment Role
    role = relationship("AssessmentRole", back_populates="indicators")

    # Relationship with Evidences
    evidences = relationship("Evidence", back_populates="indicator")