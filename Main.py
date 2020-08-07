
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from forms import MakeMoveForm
import redis
import random 
import json
app = Flask(__name__)
app.config.from_object('config.Config')



r = redis.Redis()
r.set("name",'karl')
print(r.get("name"))
r.set("score", 0)

@app.route("/")
def index():
	return render_template('homepage.html')

@app.route("/hello")
def hello():
	return render_template('board_page.html')

@app.route("/formtest", methods=('GET', 'POST'))
def board():
	key = random.randint(0,1000)

	form = MakeMoveForm()
	print("Here")
	if request.method == "POST":
		result = request.form
		print(result)
		print(result['row'])
		r.incrby("score", result['row'])
		print(r.get("score"))
		return redirect(url_for('bio'))
	return render_template('basic_form.html', form=form, key=key)


@app.route("/bio")
def bio():
	return "Karl is a cool dude"


@app.route("/XMLTest", methods=("GET", "POST"))
def XMLTest():
	if not r.exists('player1key'):
		r.set('player1key', random.randint(0,1000))	
	
	print(r.get('player1key'))
	if request.method == "POST":
		print("In Post Request")
		print(request.data)
		print(type(request.data))
		newObj = json.loads(request.data)
		print(newObj["skey"])
		r.incrby("score", newObj["tile"])
		return redirect(url_for("update"))
		
		

	
	return render_template('HTTPTest.html', key=r.get('player1key').decode('utf-8'))


@app.route("/XMLTest/update")
def update():
	state = {
	"current":  str(r.get("score")),
	"phase" : "Playing"
	}
	obj = json.dumps(state)
	print(obj)
	print(type(obj))
	return obj


if __name__ == "__main__":
	app.run()
