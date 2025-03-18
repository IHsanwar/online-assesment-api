from sqlalchemy.orm import Session
from Models.Connection import SessionLocal
from Models.Indicators import Indicator

class IndicatorController:
    def __init__(self):
        self.session = SessionLocal()

    def get_all_indicators(self):
        indicators = self.session.query(Indicator).all()
        return [
            {
                "id": i.id,
                "role_id": i.role_id,
                "assessment_tool": i.assessment_tool,
                "description": i.description,
                "indicator_item": i.indicator_item
            }
            for i in indicators
        ]

    def get_indicator_by_id(self, indicator_id):
        indicator = self.session.query(Indicator).filter_by(id=indicator_id).first()
        if indicator:
            return {
                "id": indicator.id,
                "role_id": indicator.role_id,
                "assessment_tool": indicator.assessment_tool,
                "description": indicator.description,
                "indicator_item": indicator.indicator_item
            }
        return None

    def add_indicator(self, role_id, assessment_tool, description, indicator_item):
        new_indicator = Indicator(
            role_id=role_id,
            assessment_tool=assessment_tool,
            description=description,
            indicator_item=indicator_item
        )
        self.session.add(new_indicator)
        self.session.commit()
        return {"message": "Indicator added successfully", "id": new_indicator.id}, 201

    def update_indicator(self, indicator_id, role_id, assessment_tool, description, indicator_item):
        indicator = self.session.query(Indicator).filter_by(id=indicator_id).first()
        if not indicator:
            return {"error": "Indicator not found"}, 404

        indicator.role_id = role_id
        indicator.assessment_tool = assessment_tool
        indicator.description = description
        indicator.indicator_item = indicator_item
        self.session.commit()
        return {"message": "Indicator updated successfully"}

    def delete_indicator(self, indicator_id):
        indicator = self.session.query(Indicator).filter_by(id=indicator_id).first()
        if not indicator:
            return {"error": "Indicator not found"}, 404

        self.session.delete(indicator)
        self.session.commit()
        return {"message": "Indicator deleted successfully"}
