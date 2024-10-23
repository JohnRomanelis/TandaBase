# app/routes/orchestra.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.orchestra_forms import OrchestraForm
from app.services.orchestra_service import OrchestraService

orchestra_bp = Blueprint('orchestra_bp', __name__)

@orchestra_bp.route('/add', methods=['GET', 'POST'])
def add_orchestra():
    form = OrchestraForm()
    if form.validate_on_submit():
        OrchestraService.create_orchestra(
            name=form.name.data,
            is_modern=form.is_modern.data
        )
        flash('Orchestra added successfully!', 'success')
        return redirect(url_for('orchestra_bp.list_orchestras'))
    return render_template('orchestra/add_orchestra.html', form=form)

@orchestra_bp.route('/')
def list_orchestras():
    orchestras = OrchestraService.get_all_orchestras()
    return render_template('orchestra/list_orchestras.html', orchestras=orchestras)
