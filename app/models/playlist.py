# app/models/playlist.py
from app.extensions import db
from .associations import playlist_tandas

class Playlist(db.Model):
    __tablename__ = 'playlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    tandas = db.relationship('Tanda', secondary=playlist_tandas, backref='playlists', order_by=playlist_tandas.c.order)

    def __repr__(self):
        return f"<Playlist {self.name}>"
