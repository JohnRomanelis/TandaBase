# app/forms/tanda_forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Optional, URL
from app.models.type import Type
from app.extensions import db

def get_type_choices():
    return [(t.id, t.name) for t in Type.query.order_by('name').all()]

class TandaForm(FlaskForm):
    name = StringField('Tanda Name', validators=[DataRequired()])
    tanda_type_id = SelectField('Type', coerce=int, validators=[DataRequired()])
    comments = TextAreaField('Comments', validators=[Optional()])
    spotify_link = StringField('Spotify Link', validators=[Optional(), URL()])
    youtube_link = StringField('YouTube Link', validators=[Optional(), URL()])
    song_ids = HiddenField('Song IDs')  # This will store song IDs in order
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(TandaForm, self).__init__(*args, **kwargs)
        self.tanda_type_id.choices = get_type_choices()
