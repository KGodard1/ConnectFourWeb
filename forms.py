from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import SubmitField

class MakeMoveForm(FlaskForm):
    row = IntegerField("Into which row will you play?")
    submit = SubmitField('Submit')
