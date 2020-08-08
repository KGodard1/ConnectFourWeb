

var canvas = document.getElementById('myCanvas');
var ctx = canvas.getContext("2d");
var unit = canvas.width / 26;


var arr = new Array(42).fill(0);


drawBoard(arr);



function makeMove(lane, key, gameID) {
	var move_data = {"gameID":gameID, "secret_key":key, "lane":lane}
	var update_url = '/game/makemove';

	let fetchPromise = fetch(update_url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json;charset=utf-8'
		},
		body: JSON.stringify(move_data)
	});
	fetchPromise.then(response => {
		return response.json();
	}).then(status => {
		handleMoveResponse(status);
	});
}

function handleMoveResponse(update) {
	if (update["move_made"] == 0) {
		console.log(update);
		return 0;
	}
	console.log(update["board"]);
	drawBoard(update["board"])
	console.log(update);
	return 1;
}

function getUpdate(){

}

function drawBoard(boardstate) {
	for (var i = 0; i < 42; i++) {
		var x = i % 7;
		var startx = unit * (5/2 + 7 * x / 2);
		var y = Math.floor(i/7);
		var starty = unit * (13/7 + 20 * y / 7);
		ctx.beginPath();
		ctx.arc(startx, starty, unit, 0, 2 * Math.PI);
		if (boardstate[i] == 0) {
			ctx.fillStyle = "lightblue";
		} else if (boardstate[i] == 1) {
			ctx.fillStyle = "red";
		} else if (boardstate[i] == 2) {
			ctx.fillStyle = "blue";
		} else {
			ctx.fillStyle = "black";
		}
		
		ctx.fill();
		ctx.fillStyle = "black";
		ctx.stroke();
	}
} 













/*
function placeTile(lane, turn, arr) {
	if (arr[lane] != 0) {
		return false; 
	}
	
	for (var i = 5; i >=0; i--) {
		if (arr[lane +7*i] == 0) {
			arr[lane + 7 * i] = turn;
			return lane + 7*i;
		}
	}
	
}
*/
/*
function checkForWin(boardState, lastMove) {
	p = lastMove;
	if (p % 7 < 4) {
		if(checkSequence(boardState, lastMove, 1)) {return boardState[lastMove];}
	}
	if (p % 7 > 2) {
		if(checkSequence(boardState, lastMove, -1)) {return boardState[lastMove];}
	}
	if (p - 21 < 0) {
		if(checkSequence(boardState, lastMove, 7)) {return boardState[lastMove];}
	}
	if (p + 21 > 41) {
		if(checkSequence(boardState, lastMove, -7)) {return boardState[lastMove];}
	}
	if (p % 7 < 4 && p / 7 >= 3) {
		if(checkSequence(boardState, lastMove, -6)) {return boardState[lastMove];}
	}
	if (p % 7 < 4 && p / 7 < 3) {
		if(checkSequence(boardState, lastMove, 8)) {return boardState[lastMove];}
	}
	if (p %	 7 < 4 && p / 7 >= 3) {
		if(checkSequence(boardState, lastMove, -8)) {return boardState[lastMove];}
	}
	if (p % 7 > 2 && p / 7 < 3) {
		if(checkSequence(boardState, lastMove, 6)) {return boardState[lastMove];}
	}
	return false;
}
*/
/*
function checkSequence(boardState, move, step) {
	for (var i = 1; i < 4; i++) {
		if(boardState[move] != boardState[move + step * i]) {
			return false;
		}
	}
	return true;
}
*/