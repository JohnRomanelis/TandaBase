# app/models/singer.py
from app.extensions import db
from .associations import song_singers
from sqlalchemy import Enum

class Singer(db.Model):
    __tablename__ = 'singer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    sex = db.Column(
        Enum('Male', 'Female', 'Other', name='sex_enum'),
        nullable=False
    )

    songs = db.relationship('Song', secondary=song_singers, back_populates='singers')

    def __repr__(self):
        return f"<Singer {self.name} ({self.sex})>"
