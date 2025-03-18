from Models.Connection import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey,Text, Date
from sqlalchemy.orm import relationship

class Sector(Base):
    __tablename__ = 'sectors'

    id = Column(Integer, primary_key=True, nullable=False)
    code = Column(String(6), nullable=False)
    name = Column(String(160), nullable=False)
    description = Column(Text)

    # Relationship with Job Levels
    job_levels = relationship("JobLevel", back_populates="sector")