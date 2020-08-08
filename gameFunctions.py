


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
			return (col + 7 * row);
	return "error"	

def checkValidMove(gameBoard, col):
	return True

def checkForTie(gameBoard):
	return False


def checkForWin(gameBoard, turn):
	return False