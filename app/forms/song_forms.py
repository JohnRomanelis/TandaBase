# app/forms/song_forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, NumberRange, URL
from app.models.type import Type
from app.models.style import Style
from app.models.orchestra import Orchestra
from app.models.singer import Singer
from app.extensions import db

def get_type_choices():
    return [(t.id, t.name) for t in Type.query.order_by('name').all()]

def get_style_choices():
    return [(s.id, s.name) for s in Style.query.order_by('name').all()]

def get_orchestra_choices():
    return [(o.id, o.name) for o in Orchestra.query.order_by('name').all()]

def get_singer_choices():
    return [(s.id, s.name) for s in Singer.query.order_by('name').all()]

class SongForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    orchestra_id = SelectField('Orchestra', coerce=int, validators=[DataRequired()])
    recording_year = IntegerField('Recording Year', validators=[Optional(), NumberRange(min=1800, max=2100)])
    is_instrumental = BooleanField('Instrumental')
    spotify_link = StringField('Spotify Link', validators=[Optional(), URL()])
    youtube_link = StringField('YouTube Link', validators=[Optional(), URL()])
    duration_seconds = IntegerField('Duration (seconds)', validators=[Optional(), NumberRange(min=0)])
    type_id = SelectField('Type', coerce=int, validators=[DataRequired()])
    style_id = SelectField('Style', coerce=int, validators=[Optional()])
    singer_ids = SelectMultipleField('Singers', coerce=int, validators=[Optional()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        self.type_id.choices = get_type_choices()
        self.style_id.choices = [(0, '--- Select Style ---')] + get_style_choices()
        self.orchestra_id.choices = get_orchestra_choices()
        self.singer_ids.choices = get_singer_choices()


class SongSearchForm(FlaskForm):
    title = StringField('Title', validators=[Optional()])
    orchestra = StringField('Orchestra', validators=[Optional()])
    singer = StringField('Singer', validators=[Optional()])
    type_id = SelectField('Type', coerce=int, validators=[Optional()])
    style_id = SelectField('Style', coerce=int, validators=[Optional()])
    year_from = IntegerField('Year From', validators=[Optional(), NumberRange(min=0, max=9999)])
    year_to = IntegerField('Year To', validators=[Optional(), NumberRange(min=0, max=9999)])
    submit = SubmitField('Search')

    def __init__(self, *args, **kwargs):
        super(SongSearchForm, self).__init__(*args, **kwargs)
        self.type_id.choices = get_type_choices()
        self.style_id.choices = get_style_choices()