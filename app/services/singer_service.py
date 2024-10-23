# app/services/singer_service.py

from app.models.singer import Singer
from app.extensions import db

class SingerService:
    @staticmethod
    def create_singer(data):
        # Validate required fields
        required_fields = ['name', 'sex']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"{field} is required.")

        singer = Singer(
            name=data['name'],
            sex=data['sex']
        )
        db.session.add(singer)
        db.session.commit()
        return singer

    @staticmethod
    def get_singer(singer_id):
        return Singer.query.get(singer_id)

    @staticmethod
    def update_singer(singer_id, data):
        singer = Singer.query.get(singer_id)
        if not singer:
            return None

        if 'name' in data:
            singer.name = data['name']

        if 'sex' in data:
            singer.sex = data['sex']

        db.session.commit()
        return singer

    @staticmethod
    def delete_singer(singer_id):
        singer = Singer.query.get(singer_id)
        if not singer:
            return False
        db.session.delete(singer)
        db.session.commit()
        return True

    @staticmethod
    def get_all_singers():
        return Singer.query.order_by(Singer.name).all()
