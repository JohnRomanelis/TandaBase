# app/models/song.py
from app.extensions import db
from .associations import song_singers
from sqlalchemy.orm import validates

class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    orchestra_id = db.Column(db.Integer, db.ForeignKey('orchestra.id'), nullable=False)
    recording_year = db.Column(db.Integer)
    is_instrumental = db.Column(db.Boolean, default=False)
    spotify_link = db.Column(db.String(200))
    youtube_link = db.Column(db.String(200))
    duration_seconds = db.Column(db.Integer)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'))

    orchestra = db.relationship('Orchestra', back_populates='songs')
    type = db.relationship('Type', back_populates='songs')
    style = db.relationship('Style', back_populates='songs')
    singers = db.relationship('Singer', secondary=song_singers, back_populates='songs')

    def __repr__(self):
        return f"<Song {self.title}>"

    @validates('style_id')
    def validate_style(self, key, value):
        if value:
            if self.type.name != 'Tango':
                raise ValueError("Style can only be set if the song type is 'Tango'")
        return value
