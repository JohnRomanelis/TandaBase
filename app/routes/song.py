# app/routes/song.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.forms.song_forms import SongForm
from app.forms.delete_form import DeleteForm
from app.services.song_service import SongService
from app.services.orchestra_service import OrchestraService
from app.services.singer_service import SingerService
from app.services.type_and_style_service import TypeService, StyleService


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
    # Fetch required data for the search box
    orchestras = OrchestraService.get_all_orchestras()
    singers = SingerService.get_all_singers()
    types = TypeService.get_all_types()
    styles = StyleService.get_all_styles()


    songs = SongService.get_all_songs()
    delete_form = DeleteForm()
    return render_template('song/list_songs.html', 
                            songs=songs, 
                            orchestras=orchestras,
                            singers=singers,
                            types=types,
                            styles=styles,
                            delete_form=delete_form)

@song_bp.route('/view/<int:song_id>')
def view_song(song_id):
    song = SongService.get_song(song_id)
    if not song:
        flash('Song not found.', 'danger')
        return redirect(url_for('song_bp.list_songs'))
    return render_template('song/view_song.html', song=song)

@song_bp.route('/songs/search')
def search_results():
    # Get search parameters from query string
    name = request.args.get('name', '').strip()
    orchestra_id = request.args.get('orchestra_id', '')
    singer_id = request.args.get('singer_id', '')
    type_id = request.args.get('type_id', '')
    style_id = request.args.get('style_id', '')
    year_from = request.args.get('year_from', '')
    year_to = request.args.get('year_to', '')

    # Perform search using the service layer
    search_params = {
        'name': name,
        'orchestra_id': orchestra_id,
        'singer_id': singer_id,
        'type_id': type_id,
        'style_id': style_id,
        'year_from': year_from,
        'year_to': year_to
    }
    songs = SongService.search_songs(search_params)

    # Fetch required data for the search box
    orchestras = OrchestraService.get_all_orchestras()
    singers = SingerService.get_all_singers()
    types = TypeService.get_all_types()
    styles = StyleService.get_all_styles()

    delete_form = DeleteForm()
    return render_template(
        'song/list_songs.html',
        songs=songs,
        orchestras=orchestras,
        singers=singers,
        types=types,
        styles=styles,
        delete_form=delete_form
    )

@song_bp.route('/songs/search_json')
def search_songs_json():
    # Get search parameters from query string
    name = request.args.get('name', '').strip()
    orchestra_id = request.args.get('orchestra_id', '')
    singer_id = request.args.get('singer_id', '')
    type_id = request.args.get('type_id', '')
    style_id = request.args.get('style_id', '')
    year_from = request.args.get('year_from', '')
    year_to = request.args.get('year_to', '')

    # Perform search using the service layer
    search_params = {
        'name': name,
        'orchestra_id': orchestra_id,
        'singer_id': singer_id,
        'type_id': type_id,
        'style_id': style_id,
        'year_from': year_from,
        'year_to': year_to
    }
    songs = SongService.search_songs(search_params)

    # Return JSON with all relevant song attributes
    results = []
    for song in songs:
        results.append({
            'id': song.id,
            'title': song.title,
            'type': song.type.name,                # Assuming `song.type` is a relationship to a `Type` model
            'style': song.style.name if song.style else 'N/A', # Assuming style can be null
            'singers': [singer.name for singer in song.singers],
            'recording_year': song.recording_year,
            'orchestra': song.orchestra.name if song.orchestra else 'Unknown'
        })
    return jsonify(results)     