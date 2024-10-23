from app.extensions import db

# Association table for song_singers
song_singers = db.Table(
    'song_singers',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('singer_id', db.Integer, db.ForeignKey('singer.id'), primary_key=True)
)

# Association table for tanda_songs
tanda_songs = db.Table(
    'tanda_songs',
    db.Column('tanda_id', db.Integer, db.ForeignKey('tanda.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('order', db.Integer)
)

# Association table for playlist_tandas
playlist_tandas = db.Table(
    'playlist_tandas',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('tanda_id', db.Integer, db.ForeignKey('tanda.id'), primary_key=True),
    db.Column('order', db.Integer)
)

# Association table for user_playlists
# user_playlists = db.Table(
#     'user_playlists',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
# )
