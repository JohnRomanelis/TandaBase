# app/services/song_service.py

from app.models.song import Song
from app.models.orchestra import Orchestra
from app.models.type import Type
from app.models.style import Style
from app.models.singer import Singer
from app.extensions import db

class SongService:
    @staticmethod
    def create_song(data):
        # Validate required fields
        required_fields = ['title', 'orchestra_id', 'type_id']
        for d in data:
            print(d)
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"{field} is required.")

        # Fetch related entities
        orchestra = Orchestra.query.get(data['orchestra_id'])
        if not orchestra:
            raise ValueError("Invalid orchestra ID.")

        song_type = Type.query.get(data['type_id'])
        if not song_type:
            raise ValueError("Invalid type ID.")

        style = None
        if data.get('style_id'):
            style = Style.query.get(data['style_id'])
            if not style:
                raise ValueError("Invalid style ID.")
            if song_type.name != 'Tango':
                raise ValueError("Style can only be set if the song type is 'Tango'.")

        singers = []
        if data.get('singer_ids'):
            singers = Singer.query.filter(Singer.id.in_(data['singer_ids'])).all()

        # Create the song
        song = Song(
            title=data['title'],
            orchestra=orchestra,
            recording_year=data.get('recording_year'),
            is_instrumental=data.get('is_instrumental', False),
            spotify_link=data.get('spotify_link'),
            youtube_link=data.get('youtube_link'),
            duration_seconds=data.get('duration_seconds'),
            type=song_type,
            style=style,
            singers=singers
        )
        db.session.add(song)
        db.session.commit()
        return song

    @staticmethod
    def get_song(song_id):
        return Song.query.get(song_id)

    @staticmethod
    def update_song(song_id, data):
        song = Song.query.get(song_id)
        if not song:
            return None

        # Update fields
        if 'title' in data:
            song.title = data['title']

        if 'orchestra_id' in data:
            orchestra = Orchestra.query.get(data['orchestra_id'])
            if not orchestra:
                raise ValueError("Invalid orchestra ID.")
            song.orchestra = orchestra

        if 'type_id' in data:
            song_type = Type.query.get(data['type_id'])
            if not song_type:
                raise ValueError("Invalid type ID.")
            song.type = song_type

            # Reset style if type is not Tango
            if song_type.name != 'Tango':
                song.style = None

        if 'style_id' in data:
            if data['style_id']:
                style = Style.query.get(data['style_id'])
                if not style:
                    raise ValueError("Invalid style ID.")
                if song.type.name != 'Tango':
                    raise ValueError("Style can only be set if the song type is 'Tango'.")
                song.style = style
            else:
                song.style = None

        if 'recording_year' in data:
            song.recording_year = data['recording_year']

        if 'is_instrumental' in data:
            song.is_instrumental = data['is_instrumental']

        if 'spotify_link' in data:
            song.spotify_link = data['spotify_link']

        if 'youtube_link' in data:
            song.youtube_link = data['youtube_link']

        if 'duration_seconds' in data:
            song.duration_seconds = data['duration_seconds']

        if 'singer_ids' in data:
            singers = Singer.query.filter(Singer.id.in_(data['singer_ids'])).all()
            song.singers = singers

        db.session.commit()
        return song

    @staticmethod
    def delete_song(song_id):
        song = Song.query.get(song_id)
        if not song:
            return False
        db.session.delete(song)
        db.session.commit()
        return True

    @staticmethod
    def get_all_songs():
        return Song.query.order_by(Song.title).all()


    @staticmethod
    def search_songs(params):
        query = Song.query

        # Filter by name
        if params.get('name'):
            query = query.filter(Song.title.ilike(f"%{params['name']}%"))

        # Filter by orchestra
        if params.get('orchestra_id'):
            query = query.filter(Song.orchestra_id == params['orchestra_id'])

        # Filter by singer
        if params.get('singer_id'):
            query = query.join(Song.singers).filter(Singer.id == params['singer_id'])

        # Filter by type
        if params.get('type_id'):
            query = query.filter(Song.type_id == params['type_id'])

        # Filter by style
        if params.get('style_id'):
            query = query.filter(Song.style_id == params['style_id'])

        # Filter by year range
        year_from = params.get('year_from')
        year_to = params.get('year_to')
        if year_from:
            query = query.filter(Song.recording_year >= int(year_from))
        if year_to:
            query = query.filter(Song.recording_year <= int(year_to))

        # Execute query
        return query.order_by(Song.title).all()