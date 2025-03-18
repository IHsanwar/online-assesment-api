from sqlalchemy.orm import Session
from Models.Connection import SessionLocal
from Models.CompetencyCategory import CompetencyCategory

class CompetencyCategoryController:
    def __init__(self):
        self.session = SessionLocal()

    def get_all_categories(self):
        categories = self.session.query(CompetencyCategory).all()
        return [{"category_id": c.category_id, "category_name": c.category_name} for c in categories]

    def get_category_by_id(self, category_id):
        category = self.session.query(CompetencyCategory).filter_by(category_id=category_id).first()
        if category:
            return {"category_id": category.category_id, "category_name": category.category_name}
        return None

    def add_category(self, category_name):
        existing_category = self.session.query(CompetencyCategory).filter_by(category_name=category_name).first()
        if existing_category:
            return {"error": "Category already exists"}, 400
        
        new_category = CompetencyCategory(category_name=category_name)
        self.session.add(new_category)
        self.session.commit()
        return {"message": "Category added successfully", "category_id": new_category.category_id}, 201

    def update_category(self, category_id, category_name):
        category = self.session.query(CompetencyCategory).filter_by(category_id=category_id).first()
        if not category:
            return {"error": "Category not found"}, 404

        category.category_name = category_name
        self.session.commit()
        return {"message": "Category updated successfully"}

    def delete_category(self, category_id):
        category = self.session.query(CompetencyCategory).filter_by(category_id=category_id).first()
        if not category:
            return {"error": "Category not found"}, 404

        self.session.delete(category)
        self.session.commit()
        return {"message": "Category deleted successfully"}
