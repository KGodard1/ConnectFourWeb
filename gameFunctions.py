


def update_board(gameBoard, col, turn):	
	if turn == "p1":
		color = 1
	elif turn == "p2":
		color = 2
	else:
		color = 3
	for row in range(5,-1, -1):
		if (gameBoard[col +7*row] == 0):
			print(col + 7*row)
			gameBoard[col + 7 * row] = color
			return [col + 7 * row, color];
	return "error"	

def checkValidMove(gameBoard, col):
	for row in range(5, -1. -1):
		if (gameBoard[col +7*row] == 0):
			return True
	return False

def checkForTie(gameBoard):
	if 0 in gameBoard:
		return False
	else:
		return True	


def checkForWin(gameBoard, turn):
	return False