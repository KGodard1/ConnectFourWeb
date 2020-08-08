import math


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
	for row in range(5, -1, -1):
		if (gameBoard[col +7*row] == 0):
			return True
	return False

def checkForTie(gameBoard):
	if 0 in gameBoard:
		return False
	else:
		return True	


def checkForWin(gameBoard, move, turn):
	b = [[gameBoard[7*row + col]  for col in range(0,7)] for row in range(0,6)]
	print(b)
	y = math.floor(move / 7)
	x = move % 7
	distanceInDirection = [0] * 7 #direction 0 is upper right tile, rotates clockwise
	directionalMovement = {0:(-1,1), 1:(0, 1), 2:(1,1), 3:(1,0), 4:(1,-1), 5:(0,-1), 6:(-1,-1)}
	directionsToSearch = range(0,7)
	directionsRemaining = []
	counter = 1
	while directionsToSearch != []:
		print("Testing")
		print(directionsToSearch)
		for d in directionsToSearch:
			new_y = y + counter * directionalMovement[d][0]
			new_x = x + counter * directionalMovement[d][1]
			if new_y > 5 or new_y < 0 or new_x >6 or new_x <0:
				pass
			elif b[new_y][new_x] != turn:
				pass
			else:
				directionsRemaining.append(d)
				distanceInDirection[d] += 1
		print(directionsRemaining)
		directionsToSearch = directionsRemaining
		directionsRemaining = []
		counter+= 1
	d1 = (distanceInDirection[0] + distanceInDirection[4]) >= 3
	d2 = (distanceInDirection[1] + distanceInDirection[5]) >= 3
	d3 = (distanceInDirection[2] + distanceInDirection[6]) >= 3
	d4 = (distanceInDirection[3]) >= 4
	if d1 or d2 or d3 or d4:
		return True
	else:
		return False

