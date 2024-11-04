# app/routes/tanda.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.forms.tanda_forms import TandaForm
from app.forms.delete_form import DeleteForm
from app.services.tanda_service import TandaService
from app.services.song_service import SongService
from app.services.orchestra_service import OrchestraService
from app.services.singer_service import SingerService
from app.services.type_and_style_service import TypeService, StyleService

tanda_bp = Blueprint('tanda_bp', __name__)

@tanda_bp.route('/', methods=['GET'])
def list_tandas():
    tandas = TandaService.get_all_tandas()
    delete_form = DeleteForm()
    return render_template('tanda/list_tandas.html', tandas=tandas, delete_form=delete_form)

@tanda_bp.route('/create', methods=['GET', 'POST'])
def create_tanda():
    print("Form submission received")  # Check if any request hits this route

    form = TandaForm()
    print(form.errors)
    if form.validate_on_submit():
        print("We are in the create_tanda route") 

        # preprocess the song IDS 
        #TODO: This looks like a workaround. Need to check if there is a better way to do this.
        song_ids = request.form.getlist('song_ids')[0].split(',')
        song_ids = [int(song_id) for song_id in song_ids]
        
        data = {
            'name': form.name.data,
            'tanda_type_id': form.tanda_type_id.data,
            'comments': form.comments.data,
            'spotify_link': form.spotify_link.data,
            'youtube_link': form.youtube_link.data,
            'song_ids': song_ids
        }
        print(data)
        TandaService.create_tanda(data)
        flash('Tanda created successfully!', 'success')
        return redirect(url_for('tanda_bp.list_tandas'))
    print(form.errors)
    # Fetch required data for the search box
    orchestras = OrchestraService.get_all_orchestras()
    singers = SingerService.get_all_singers()
    types = TypeService.get_all_types()
    styles = StyleService.get_all_styles()
    return render_template('tanda/create_tanda.html', form=form, orchestras=orchestras, singers=singers, types=types, styles=styles)

@tanda_bp.route('/edit/<int:tanda_id>', methods=['GET', 'POST'])
def edit_tanda(tanda_id):
    tanda = TandaService.get_tanda(tanda_id)
    if not tanda:
        flash('Tanda not found.', 'danger')
        return redirect(url_for('tanda_bp.list_tandas'))

    form = TandaForm(obj=tanda)
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'tanda_type_id': form.tanda_type_id.data,
            'comments': form.comments.data,
            'spotify_link': form.spotify_link.data,
            'youtube_link': form.youtube_link.data,
            'song_ids': request.form.get('song_ids', '').split(',')
        }
        TandaService.update_tanda(tanda_id, data)
        flash('Tanda updated successfully!', 'success')
        return redirect(url_for('tanda_bp.list_tandas'))

    # Prepare preloaded songs data, ensuring all values are defined
    preloaded_songs = []
    for song in tanda.songs:
        song_dict = {
            'id': song.id,
            'title': song.title or '',
            'orchestra': song.orchestra.name if song.orchestra and song.orchestra.name else ''
        }
        preloaded_songs.append(song_dict)

    return render_template('tanda/edit_tanda.html', form=form, tanda=tanda, preloaded_songs=preloaded_songs)

@tanda_bp.route('/view/<int:tanda_id>', methods=['GET'])
def view_tanda(tanda_id):
    tanda = TandaService.get_tanda(tanda_id)
    if not tanda:
        flash('Tanda not found.', 'danger')
        return redirect(url_for('tanda_bp.list_tandas'))
    return render_template('tanda/view_tanda.html', tanda=tanda)

@tanda_bp.route('/delete/<int:tanda_id>', methods=['POST'])
def delete_tanda(tanda_id):
    success = TandaService.delete_tanda(tanda_id)
    if success:
        flash('Tanda deleted successfully!', 'success')
    else:
        flash('Tanda not found.', 'danger')
    return redirect(url_for('tanda_bp.list_tandas'))

# Additional route to search songs (for adding to tanda)
@tanda_bp.route('/search_songs', methods=['GET'])
def search_songs():
    query = request.args.get('q', '')
    songs = SongService.search_songs(query)
    songs_data = [{'id': song.id, 'title': song.title, 'orchestra': song.orchestra.name} for song in songs]
    return jsonify(songs_data)
