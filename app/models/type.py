# app/models/type.py
from app.extensions import db

class Type(db.Model):
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    songs = db.relationship('Song', back_populates='type')
    tandas = db.relationship('Tanda', back_populates='type')

    def __repr__(self):
        return f"<Type {self.name}>"
