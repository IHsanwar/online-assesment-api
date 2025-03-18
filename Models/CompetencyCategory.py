from Models.Connection import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, Date, UniqueConstraint
from sqlalchemy.orm import relationship


class CompetencyCategory(Base):
    __tablename__ = 'competency_categories'

    category_id = Column(Integer, primary_key=True, nullable=False)
    category_name = Column(String(50), nullable=False)
    core = Column(Enum('CORE', 'TEAM', 'MANA', 'SOSC'), nullable=False)
    description = Column(String(300))

    competency_keys = relationship("CompetencyKey", back_populates="category")

