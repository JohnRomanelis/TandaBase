# app/models/style.py
from app.extensions import db

class Style(db.Model):
    __tablename__ = 'style'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    songs = db.relationship('Song', back_populates='style')

    def __repr__(self):
        return f"<Style {self.name}>"
