# app/forms/orchestra_forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class OrchestraForm(FlaskForm):
    name = StringField('Orchestra Name', validators=[DataRequired()])
    is_modern = BooleanField('Is Modern?')
    submit = SubmitField('Submit')
