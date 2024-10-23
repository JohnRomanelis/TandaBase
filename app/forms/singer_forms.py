# app/forms/singer_forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class SingerForm(FlaskForm):
    name = StringField('Singer Name', validators=[DataRequired()])
    sex = SelectField(
        'Sex',
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
