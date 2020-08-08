
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from forms import MakeMoveForm, MakeNewGameButton, JoinGameForm
from gameFunctions import update_board, checkValidMove, checkForTie, checkForWin			
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
		r.hset(gameInfo, "turn", "p1")#random.choice(["p1", "p2"]))
		while r.llen(gameBoard) < 42:
			r.rpush(gameBoard, 0)

	return render_template("game.html", key = code, phase=r.hget(gameInfo, "phase"), gameID=gameID)


@app.route("/game/makemove", methods=['POST'])
def makemove():
	if request.method == "POST":
		moveData = json.loads(request.data)
		gameData = "game:" + moveData["gameID"]
		boardData = "board:" + moveData["gameID"]

		turnToMove = r.hget(gameData, "turn").decode('utf-8')
		print(turnToMove)
		print(moveData['secret_key'])
		print(r.hget(gameData, turnToMove))
		if r.hget(gameData, "phase").decode('utf-8') != "playing":
			fail_data = {"move_made":False, "reason":"game not in session"}
			fail_json = json.dumps(fail_data)
			return fail_json

		if moveData['secret_key'] != r.hget(gameData, turnToMove).decode('utf-8'):
			fail_data = {"move_made":False, "reason":"out of turn"}
			fail_json = json.dumps(fail_data)
			return fail_json

		board = [int(tile) for tile in r.lrange(boardData, 0, -1)]
		print(board)
		column = moveData["lane"]
		print(column)

		if not checkValidMove(board, column):
			fail_data = {"move_made":False, "reason":"invalid move"}
			fail_json = json.dumps(fail_data)
			return fail_json
		
		
		move = update_board(board, column, turnToMove)
		board[move[0]] = move[1]
		r.lset(boardData, move[0], move[1])


		if turnToMove == "p1":
			r.hset(gameData, "turn", "p2")
		else:
			r.hset(gameData, "turn", "p1")

		
		if checkForWin(board, move[0], move[1]):
			win_data = {"move_made":True, "phase": "end", "outcome": turnToMove, "board": board}
			win_json = json.dumps(win_data)
			return win_json
		elif checkForTie(board):
			tie_data = {"move_made":True, "phase":"end", "outcome":"tie", "board": board}
			tie_json = json.dumps(tie_data)
			return tie_json
		else:
			neutral_data = {"move_made":True, "phase": "playing", "outcome":"still playing", "board": board}
			neutral_json = json.dumps(neutral_data)
			return neutral_json

@app.route("/game/getUpdate/<gameID>")
def getUpdate(gameID):
	gameData = "game:" + str(gameID)
	boardData = "board:" + str(gameID)
	phase = r.hget(gameData, "phase").decode('utf-8')
	board = [int(tile) for tile in r.lrange(boardData, 0, -1)]
	updateData = {"phase": phase, "board": board}
	updateJson = json.dumps(updateData)
	return updateJson


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
