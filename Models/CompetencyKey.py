from Models.Connection import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Date, UniqueConstraint
from sqlalchemy.orm import relationship

class CompetencyKey(Base):
    __tablename__ = 'competency_key'

    key_id = Column(Integer, primary_key=True, nullable=False)
    key_code = Column(String(12), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('competency_categories.category_id'), nullable=False)
    competency_name = Column(String, nullable=False)

    # Relationship with CompetencyCategory
    category = relationship("CompetencyCategory", back_populates="competency_keys")
