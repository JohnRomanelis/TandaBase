# app/services/playlist_service.py

from app.models.playlist import Playlist
from app.models.tanda import Tanda
from app.extensions import db
from sqlalchemy import text

class PlaylistService:
    @staticmethod
    def create_playlist(data):
        # Validate required fields
        if 'name' not in data or not data['name']:
            raise ValueError("Name is required.")

        # Fetch tandas
        tanda_ids = data.get('tanda_ids', [])
        # remove empty strings  
        tanda_ids = [int(tanda_id) for tanda_id in tanda_ids if tanda_id]
        tandas = []
        if tanda_ids:
            tandas = Tanda.query.filter(Tanda.id.in_(tanda_ids)).all()
            if len(tandas) != len(tanda_ids):
                raise ValueError("Some tandas not found.")

        # Create the playlist
        playlist = Playlist(
            name=data['name'],
            description=data.get('description'),
            spotify_link=data.get('spotify_link'),
            youtube_link=data.get('youtube_link')
        )
        db.session.add(playlist)
        db.session.commit()

        # Associate tandas with order
        for order, tanda_id in enumerate(tanda_ids):
            tanda = Tanda.query.get(tanda_id)
            db.session.execute(
                text("INSERT INTO playlist_tandas (playlist_id, tanda_id, \"order\") VALUES (:playlist_id, :tanda_id, :order)"),
                {'playlist_id': playlist.id, 'tanda_id': tanda.id, 'order': order}
            )
        db.session.commit()
        return playlist

    @staticmethod
    def get_playlist(playlist_id):
        return Playlist.query.get(playlist_id)

    @staticmethod
    def update_playlist(playlist_id, data):
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return None

        if 'name' in data:
            playlist.name = data['name']

        if 'description' in data:
            playlist.description = data['description']

        if 'spotify_link' in data:
            playlist.spotify_link = data['spotify_link']

        if 'youtube_link' in data:
            playlist.youtube_link = data['youtube_link']

        db.session.commit()

        # Update tandas
        if 'tanda_ids' in data:
            tanda_ids = data['tanda_ids']
            tandas = Tanda.query.filter(Tanda.id.in_(tanda_ids)).all()
            if len(tandas) != len(tanda_ids):
                raise ValueError("Some tandas not found.")

            # Clear existing associations
            db.session.execute(text("DELETE FROM playlist_tandas WHERE playlist_id = :playlist_id"), {'playlist_id': playlist.id})
            db.session.commit()

            # Re-associate tandas with order
            for order, tanda_id in enumerate(tanda_ids):
                tanda = Tanda.query.get(tanda_id)
                db.session.execute(
                    text("INSERT INTO playlist_tandas (playlist_id, tanda_id, \"order\") VALUES (:playlist_id, :tanda_id, :order)"),
                    {'playlist_id': playlist.id, 'tanda_id': tanda.id, 'order': order}
                )
            db.session.commit()

        return playlist

    @staticmethod
    def delete_playlist(playlist_id):
        playlist = Playlist.query.get(playlist_id)
        if not playlist:
            return False
        db.session.delete(playlist)
        db.session.commit()
        return True

    @staticmethod
    def get_all_playlists():
        return Playlist.query.order_by(Playlist.name).all()
