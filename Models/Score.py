from Models.Connection import Base  # Import Base from Connection.py
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

class Score(Base):
    __tablename__ = 'scores'

    key_id = Column(Integer, ForeignKey('competency_key.key_id'), primary_key=True, nullable=False)
    evidence_id = Column(Integer, ForeignKey('evidences.id'), primary_key=True, nullable=False)
    score = Column(Integer, nullable=False)
    scoring_date = Column(Date, nullable=False)

    # Relationships
    competency_key = relationship("CompetencyKey")
    evidence = relationship("Evidence", back_populates="scores")
