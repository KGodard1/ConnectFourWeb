
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from forms import MakeMoveForm
import redis
app = Flask(__name__)
app.config.from_object('config.Config')

r = redis.Redis()
r.set("name",'karl')
print(r.get("name"))
r.set("score", 0)


@app.route("/")
def index():
	return "Index"

@app.route("/hello")
def hello():
	return render_template('board_page.html')

@app.route("/formtest", methods=('GET', 'POST'))
def board():
	form = MakeMoveForm()
	print("Here")
	if request.method == "POST":
		result = request.form
		print(result)
		print(result['row'])
		r.incrby("score", result['row'])
		print(r.get("score"))
		return redirect(url_for('bio'))
	return render_template('basic_form.html', form=form)


@app.route("/bio")
def bio():
	return "Karl is a cool dude"


if __name__ == "__main__":
	app.run()
