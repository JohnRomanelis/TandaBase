# app/routes/song.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.song_forms import SongForm
from app.services.song_service import SongService

song_bp = Blueprint('song_bp', __name__)

@song_bp.route('/add', methods=['GET', 'POST'])
def add_song():
    form = SongForm()
    # Populate form choices
    if form.validate_on_submit():
        data = {
            'title': form.title.data,
            'orchestra_id': form.orchestra_id.data,
            # Add other fields
        }
        SongService.create_song(data)
        flash('Song added successfully!', 'success')
        return redirect(url_for('song_bp.list_songs'))
    return render_template('song/add_song.html', form=form)

@song_bp.route('/')
def list_songs():
    songs = SongService.get_all_songs()
    return render_template('song/list_songs.html', songs=songs)
