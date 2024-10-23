# app/forms/playlist_forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional

class PlaylistForm(FlaskForm):
    name = StringField('Playlist Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    tanda_ids = HiddenField('Tanda IDs')  # This will store tanda IDs in order
    submit = SubmitField('Submit')
