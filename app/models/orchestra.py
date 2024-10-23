# app/models/orchestra.py
from app.extensions import db

class Orchestra(db.Model):
    __tablename__ = 'orchestra'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    is_modern = db.Column(db.Boolean, default=False)

    songs = db.relationship('Song', back_populates='orchestra')

    def __repr__(self):
        return f"<Orchestra {self.name}>"
