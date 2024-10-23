# app/services/tanda_service.py

from app.models.tanda import Tanda
from app.models.song import Song
from app.models.type import Type
from app.extensions import db

class TandaService:
    @staticmethod
    def create_tanda(data):
        # Validate required fields
        if 'name' not in data or not data['name']:
            raise ValueError("Name is required.")

        tanda_type = Type.query.get(data['tanda_type_id'])
        if not tanda_type:
            raise ValueError("Invalid tanda type ID.")

        # Fetch songs
        song_ids = data.get('song_ids', [])
        songs = []
        if song_ids:
            songs = Song.query.filter(Song.id.in_(song_ids)).all()
            if len(songs) != len(song_ids):
                raise ValueError("Some songs not found.")

            # Ensure all songs are of the same type
            for song in songs:
                if song.type_id != tanda_type.id:
                    raise ValueError("All songs must be of the same type as the tanda.")

        # Create the tanda
        tanda = Tanda(
            name=data['name'],
            type=tanda_type,
            comments=data.get('comments'),
            spotify_link=data.get('spotify_link'),
            youtube_link=data.get('youtube_link')
        )
        db.session.add(tanda)
        db.session.commit()

        # Associate songs with order
        for order, song_id in enumerate(song_ids):
            song = Song.query.get(song_id)
            db.session.execute(
                "INSERT INTO tanda_songs (tanda_id, song_id, \"order\") VALUES (:tanda_id, :song_id, :order)",
                {'tanda_id': tanda.id, 'song_id': song.id, 'order': order}
            )
        db.session.commit()
        return tanda

    @staticmethod
    def get_tanda(tanda_id):
        return Tanda.query.get(tanda_id)

    @staticmethod
    def update_tanda(tanda_id, data):
        tanda = Tanda.query.get(tanda_id)
        if not tanda:
            return None

        if 'name' in data:
            tanda.name = data['name']

        if 'tanda_type_id' in data:
            tanda_type = Type.query.get(data['tanda_type_id'])
            if not tanda_type:
                raise ValueError("Invalid tanda type ID.")
            tanda.type = tanda_type

        if 'comments' in data:
            tanda.comments = data['comments']

        if 'spotify_link' in data:
            tanda.spotify_link = data['spotify_link']

        if 'youtube_link' in data:
            tanda.youtube_link = data['youtube_link']

        db.session.commit()

        # Update songs
        if 'song_ids' in data:
            song_ids = data['song_ids']
            songs = Song.query.filter(Song.id.in_(song_ids)).all()
            if len(songs) != len(song_ids):
                raise ValueError("Some songs not found.")

            # Ensure all songs are of the same type
            for song in songs:
                if song.type_id != tanda.type_id:
                    raise ValueError("All songs must be of the same type as the tanda.")

            # Clear existing associations
            db.session.execute("DELETE FROM tanda_songs WHERE tanda_id = :tanda_id", {'tanda_id': tanda.id})
            db.session.commit()

            # Re-associate songs with order
            for order, song_id in enumerate(song_ids):
                song = Song.query.get(song_id)
                db.session.execute(
                    "INSERT INTO tanda_songs (tanda_id, song_id, \"order\") VALUES (:tanda_id, :song_id, :order)",
                    {'tanda_id': tanda.id, 'song_id': song.id, 'order': order}
                )
            db.session.commit()

        return tanda

    @staticmethod
    def delete_tanda(tanda_id):
        tanda = Tanda.query.get(tanda_id)
        if not tanda:
            return False
        db.session.delete(tanda)
        db.session.commit()
        return True

    @staticmethod
    def get_all_tandas():
        return Tanda.query.order_by(Tanda.name).all()

    @staticmethod
    def search_tandas(query):
        return Tanda.query.filter(Tanda.name.ilike(f'%{query}%')).order_by(Tanda.name).all()
