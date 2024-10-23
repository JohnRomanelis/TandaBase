# app/routes/tanda.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.forms.tanda_forms import TandaForm
from app.services.tanda_service import TandaService
from app.services.song_service import SongService
from app.extensions import db

tanda_bp = Blueprint('tanda_bp', __name__)

@tanda_bp.route('/', methods=['GET'])
def list_tandas():
    tandas = TandaService.get_all_tandas()
    return render_template('tanda/list_tandas.html', tandas=tandas)

@tanda_bp.route('/create', methods=['GET', 'POST'])
def create_tanda():
    form = TandaForm()
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'tanda_type_id': form.tanda_type_id.data,
            'comments': form.comments.data,
            'spotify_link': form.spotify_link.data,
            'youtube_link': form.youtube_link.data,
            'song_ids': request.form.getlist('song_ids')
        }
        TandaService.create_tanda(data)
        flash('Tanda created successfully!', 'success')
        return redirect(url_for('tanda_bp.list_tandas'))
    return render_template('tanda/create_tanda.html', form=form)

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
            'song_ids': request.form.getlist('song_ids')
        }
        TandaService.update_tanda(tanda_id, data)
        flash('Tanda updated successfully!', 'success')
        return redirect(url_for('tanda_bp.list_tandas'))

    # Preload song IDs for existing tanda
    song_ids = [str(song.id) for song in tanda.songs]
    return render_template('tanda/edit_tanda.html', form=form, tanda=tanda, song_ids=song_ids)

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
