from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import SubmitField, TextField
from wtforms.validators import DataRequired
class MakeMoveForm(FlaskForm):
    row = IntegerField("Into which row will you play?")
    submit = SubmitField('Submit')

class MakeNewGameButton(FlaskForm):
	submit = SubmitField('Create Game')

class JoinGameForm(FlaskForm):
	game = TextField("Enter Code",[DataRequired()])
	submit = SubmitField("Join")