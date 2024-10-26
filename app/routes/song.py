# app/routes/song.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.song_forms import SongForm
from app.forms.delete_form import DeleteForm
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
            'recording_year': form.recording_year.data,
            'is_instrumental': form.is_instrumental.data,
            'spotify_link': form.spotify_link.data,
            'youtube_link': form.youtube_link.data,
            'duration_seconds': form.duration_seconds.data,
            'type_id': form.type_id.data,
            'style_id': form.style_id.data,
            'singer_ids': form.singer_ids.data
        }
        SongService.create_song(data)
        flash('Song added successfully!', 'success')
        return redirect(url_for('song_bp.list_songs'))
    return render_template('song/add_song.html', form=form)

@song_bp.route('/edit/<int:song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    song = SongService.get_song(song_id)
    if not song:
        flash('Song not found.', 'danger')
        return redirect(url_for('song_bp.list_songs'))

    form = SongForm(obj=song)
    if form.validate_on_submit():
        data = {
            'title': form.title.data,
            'orchestra_id': form.orchestra_id.data,
            'recording_year': form.recording_year.data,
            'is_instrumental': form.is_instrumental.data,
            'spotify_link': form.spotify_link.data,
            'youtube_link': form.youtube_link.data,
            'duration_seconds': form.duration_seconds.data,
            'type_id': form.type_id.data,
            'style_id': form.style_id.data,
            'singer_ids': form.singer_ids.data  
        }
        SongService.update_song(song_id, data)
        flash('Song updated successfully!', 'success')
        return redirect(url_for('song_bp.list_songs'))
    return render_template('song/edit_song.html', form=form, song=song)

@song_bp.route('/delete/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    try:
        success = SongService.delete_song(song_id)
        if success:
            flash('Song deleted successfully!', 'success')
        else:
            flash('Song not found.', 'danger')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('song_bp.list_songs'))

@song_bp.route('/')
def list_songs():
    songs = SongService.get_all_songs()
    delete_form = DeleteForm()
    return render_template('song/list_songs.html', songs=songs, delete_form=delete_form)

@song_bp.route('/view/<int:song_id>')
def view_song(song_id):
    song = SongService.get_song(song_id)
    if not song:
        flash('Song not found.', 'danger')
        return redirect(url_for('song_bp.list_songs'))
    return render_template('song/view_song.html', song=song)

@song_bp.route('/search', methods=['GET'])
def search_songs():
    # Get search parameters from query string
    title = request.args.get('title', '').strip()
    orchestra = request.args.get('orchestra', '').strip()
    singer = request.args.get('singer', '').strip()
    type_id = request.args.get('type_id', type=int)
    style_id = request.args.get('style_id', type=int)
    year_from = request.args.get('year_from', type=int)
    year_to = request.args.get('year_to', type=int)
    ajax = request.args.get('ajax', type=int, default=0)

    # Call the song search service with parameters
    songs = SongService.advanced_search_songs(
        title=title,
        orchestra=orchestra,
        singer=singer,
        type_id=type_id,
        style_id=style_id,
        year_from=year_from,
        year_to=year_to
    )

    if ajax:
        # Return results in JSON format
        results = []
        for song in songs:
            results.append({
                'id': song.id,
                'title': song.title,
                'orchestra': song.orchestra.name if song.orchestra else '',
                'singer': song.singer.name if song.singer else '',
                'type': song.type.name if song.type else '',
                'style': song.style.name if song.style else '',
                'year': song.year
            })
        return jsonify(results)
    else:
        # Render the song listing template with search results
        form = SongSearchForm(request.args)
        return render_template('song/list_songs.html', songs=songs, form=form)