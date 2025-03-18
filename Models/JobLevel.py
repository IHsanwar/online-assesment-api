from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Date, UniqueConstraint
from Models.Connection import Base
from sqlalchemy.orm import relationship
from Models.Sector import Sector

class JobLevel(Base):
    __tablename__ = 'job_level'

    id = Column(Integer, primary_key=True, nullable=False)
    sector_id = Column(Integer, ForeignKey('sectors.id'), nullable=False)
    code = Column(String)
    title = Column(String)

    sector = relationship("Sector", back_populates="job_levels")

    job_functions = relationship("JobFunction", back_populates="level")