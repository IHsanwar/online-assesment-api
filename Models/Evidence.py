from Models.Connection import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Date, UniqueConstraint
from sqlalchemy.orm import relationship

class Evidence(Base):
    __tablename__ = 'evidences'

    id = Column(Integer, primary_key=True, nullable=False)
    indicator_id = Column(Integer, ForeignKey('indicators.id'), nullable=False)
    evidence = Column(String)
    scored_by = Column(String)
    justification = Column(String)

    # Relationship with Indicator
    indicator = relationship("Indicator", back_populates="evidences")

    # Relationship with Scores (many-to-many)
    scores = relationship("Score", back_populates="evidence")