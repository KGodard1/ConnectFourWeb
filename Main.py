
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from forms import MakeMoveForm, MakeNewGameButton, JoinGameForm
import redis
import random 
import string
import json

app = Flask(__name__)
app.config.from_object('config.Config')



r = redis.Redis()

r.set("score", 0)

@app.route("/")
def index():
	makeGame = MakeNewGameButton()
	joinGame = JoinGameForm()
	return render_template('homepage.html', makeGameButton=makeGame,
		joinGameForm=joinGame)

@app.route("/createGame", methods=['GET', 'POST'])
def createGame():
	if request.method == "POST":
		print("here")
		result = request.form
		return redirect(url_for('game', gameID=result['game']))
	code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
	r.sadd("games", code)
	return redirect(url_for('game', gameID=code))

@app.route("/game/<gameID>")
def game(gameID):
	if not r.sismember("games", gameID):
		#RETURN BAD REQUEST
		return redirect(url_for('index'))
	gameInfo = "game:" + str(gameID)
	gameBoard = "board:" + str(gameID)
	if r.hexists(gameInfo, "p2"):
		#GAME IS FULL
		return redirect(url_for('index'))
	elif r.hexists(gameInfo, "p1"):
		code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		r.hset(gameInfo, "p2", code)
		r.hset(gameInfo, "phase", "playing")
	else:
		code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		r.hset(gameInfo, "p1", code)
		r.hset(gameInfo, "phase", "waiting")
		r.hset(gameInfo, "ID", str(gameID))
		while r.llen(gameBoard) < 42:
			r.rpush(gameBoard, 0)

	return render_template("game.html")


	return redirect(url_for('bio'))
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
