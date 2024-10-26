# app/routes/orchestra.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.orchestra_forms import OrchestraForm
from app.forms.delete_form import DeleteForm
from app.services.orchestra_service import OrchestraService

orchestra_bp = Blueprint('orchestra_bp', __name__)

@orchestra_bp.route('/add', methods=['GET', 'POST'])
def add_orchestra():
    form = OrchestraForm()
    if form.validate_on_submit():
        data = {
            'name': form.name.data,
            'is_modern': form.is_modern.data
        }
        OrchestraService.create_orchestra(data)
        flash('Orchestra added successfully!', 'success')
        return redirect(url_for('orchestra_bp.list_orchestras'))
    return render_template('orchestra/add_orchestra.html', form=form)

@orchestra_bp.route('/edit/<int:orchestra_id>', methods=['GET', 'POST'])
def edit_orchestra(orchestra_id):
    # Retrieve the orchestra by ID
    orchestra = OrchestraService.get_orchestra(orchestra_id)
    if not orchestra:
        flash('Orchestra not found.', 'danger')
        return redirect(url_for('orchestra_bp.list_orchestras'))

    # Initialize the form with the existing orchestra data
    form = OrchestraForm(obj=orchestra)

    if form.validate_on_submit():
        # Collect data from the form
        data = {
            'name': form.name.data,
            'is_modern': form.is_modern.data
        }
        # Update the orchestra using the service layer
        OrchestraService.update_orchestra(orchestra_id, data)
        flash('Orchestra updated successfully!', 'success')
        return redirect(url_for('orchestra_bp.list_orchestras'))

    return render_template('orchestra/edit_orchestra.html', form=form, orchestra=orchestra)

@orchestra_bp.route('/')
def list_orchestras():
    orchestras = OrchestraService.get_all_orchestras()
    delete_form = DeleteForm()
    return render_template('orchestra/list_orchestras.html', orchestras=orchestras, delete_form=delete_form)

@orchestra_bp.route('/delete/<int:orchestra_id>', methods=['POST'])
def delete_orchestra(orchestra_id):
    try:
        success = OrchestraService.delete_orchestra(orchestra_id)
        if success:
            flash('Orchestra deleted successfully!', 'success')
        else:
            flash('Orchestra not found.', 'danger')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('orchestra_bp.list_orchestras'))