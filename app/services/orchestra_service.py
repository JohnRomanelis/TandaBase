# app/services/orchestra_service.py

from app.models.orchestra import Orchestra
from app.extensions import db

class OrchestraService:
    @staticmethod
    def create_orchestra(data):
        # Validate required fields
        if 'name' not in data or not data['name']:
            raise ValueError("Name is required.")

        orchestra = Orchestra(
            name=data['name'],
            is_modern=data.get('is_modern', False)
        )
        db.session.add(orchestra)
        db.session.commit()
        return orchestra

    @staticmethod
    def get_orchestra(orchestra_id):
        return Orchestra.query.get(orchestra_id)

    @staticmethod
    def update_orchestra(orchestra_id, data):
        orchestra = Orchestra.query.get(orchestra_id)
        if not orchestra:
            return None

        if 'name' in data:
            orchestra.name = data['name']

        if 'is_modern' in data:
            orchestra.is_modern = data['is_modern']

        db.session.commit()
        return orchestra

    @staticmethod
    def delete_orchestra(orchestra_id):
        orchestra = Orchestra.query.get(orchestra_id)
        if not orchestra:
            return False
        db.session.delete(orchestra)
        db.session.commit()
        return True

    @staticmethod
    def get_all_orchestras():
        return Orchestra.query.order_by(Orchestra.name).all()
