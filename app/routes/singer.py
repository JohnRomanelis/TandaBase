# app/routes/singer.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.singer_forms import SingerForm
from app.services.singer_service import SingerService
from app.extensions import db

singer_bp = Blueprint('singer_bp', __name__)

@singer_bp.route('/', methods=['GET'])
def list_singers():
    singers = SingerService.get_all_singers()
    return render_template('singer/list_singers.html', singers=singers)

@singer_bp.route('/add', methods=['GET', 'POST'])
def add_singer():
    form = SingerForm()
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'sex': form.sex.data
        }
        SingerService.create_singer(data)
        flash('Singer added successfully!', 'success')
        return redirect(url_for('singer_bp.list_singers'))
    return render_template('singer/add_singer.html', form=form)

@singer_bp.route('/edit/<int:singer_id>', methods=['GET', 'POST'])
def edit_singer(singer_id):
    singer = SingerService.get_singer(singer_id)
    if not singer:
        flash('Singer not found.', 'danger')
        return redirect(url_for('singer_bp.list_singers'))

    form = SingerForm(obj=singer)
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'sex': form.sex.data
        }
        SingerService.update_singer(singer_id, data)
        flash('Singer updated successfully!', 'success')
        return redirect(url_for('singer_bp.list_singers'))
    return render_template('singer/edit_singer.html', form=form, singer=singer)

@singer_bp.route('/delete/<int:singer_id>', methods=['POST'])
def delete_singer(singer_id):
    success = SingerService.delete_singer(singer_id)
    if success:
        flash('Singer deleted successfully!', 'success')
    else:
        flash('Singer not found.', 'danger')
    return redirect(url_for('singer_bp.list_singers'))
