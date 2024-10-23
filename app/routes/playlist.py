# app/routes/playlist.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.forms.playlist_forms import PlaylistForm
from app.services.playlist_service import PlaylistService
from app.services.tanda_service import TandaService
from app.extensions import db

playlist_bp = Blueprint('playlist_bp', __name__)

@playlist_bp.route('/', methods=['GET'])
def list_playlists():
    playlists = PlaylistService.get_all_playlists()
    return render_template('playlist/list_playlists.html', playlists=playlists)

@playlist_bp.route('/create', methods=['GET', 'POST'])
def create_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'description': form.description.data,
            'tanda_ids': request.form.getlist('tanda_ids')
        }
        PlaylistService.create_playlist(data)
        flash('Playlist created successfully!', 'success')
        return redirect(url_for('playlist_bp.list_playlists'))
    return render_template('playlist/create_playlist.html', form=form)

@playlist_bp.route('/edit/<int:playlist_id>', methods=['GET', 'POST'])
def edit_playlist(playlist_id):
    playlist = PlaylistService.get_playlist(playlist_id)
    if not playlist:
        flash('Playlist not found.', 'danger')
        return redirect(url_for('playlist_bp.list_playlists'))

    form = PlaylistForm(obj=playlist)
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'description': form.description.data,
            'tanda_ids': request.form.getlist('tanda_ids')
        }
        PlaylistService.update_playlist(playlist_id, data)
        flash('Playlist updated successfully!', 'success')
        return redirect(url_for('playlist_bp.list_playlists'))

    # Preload tanda IDs for existing playlist
    tanda_ids = [str(tanda.id) for tanda in playlist.tandas]
    return render_template('playlist/edit_playlist.html', form=form, playlist=playlist, tanda_ids=tanda_ids)

@playlist_bp.route('/view/<int:playlist_id>', methods=['GET'])
def view_playlist(playlist_id):
    playlist = PlaylistService.get_playlist(playlist_id)
    if not playlist:
        flash('Playlist not found.', 'danger')
        return redirect(url_for('playlist_bp.list_playlists'))
    return render_template('playlist/view_playlist.html', playlist=playlist)

@playlist_bp.route('/delete/<int:playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    success = PlaylistService.delete_playlist(playlist_id)
    if success:
        flash('Playlist deleted successfully!', 'success')
    else:
        flash('Playlist not found.', 'danger')
    return redirect(url_for('playlist_bp.list_playlists'))

# Additional route to search tandas (for adding to playlist)
@playlist_bp.route('/search_tandas', methods=['GET'])
def search_tandas():
    query = request.args.get('q', '')
    tandas = TandaService.search_tandas(query)
    tandas_data = [{'id': tanda.id, 'name': tanda.name, 'type': tanda.type.name} for tanda in tandas]
    return jsonify(tandas_data)
