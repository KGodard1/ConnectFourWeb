
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
			r.hset(gameData,"phase", "post-game")
			win_data = {"move_made":True, "phase": "post-game", "outcome": turnToMove, "board": board}
			win_json = json.dumps(win_data)
			return win_json
		elif checkForTie(board):
			r.hset(gameData,"phase", "post-game")
			tie_data = {"move_made":True, "phase":"post-game", "outcome":"tie", "board": board}
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




if __name__ == "__main__":
	app.run()
