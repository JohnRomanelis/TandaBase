# app/models/tanda.py
from app.extensions import db
from .associations import tanda_songs

class Tanda(db.Model):
    __tablename__ = 'tanda'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    tanda_type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    comments = db.Column(db.Text)
    spotify_link = db.Column(db.String(200))
    youtube_link = db.Column(db.String(200))

    type = db.relationship('Type', back_populates='tandas')
    songs = db.relationship('Song', secondary=tanda_songs, backref='tandas', order_by=tanda_songs.c.order)

    def __repr__(self):
        return f"<Tanda {self.name}>"
