from flask import Flask
from flask import render_template, redirect, url_for, request
from chess import WebInterface, Board, MoveHistory

app = Flask(__name__)
ui = WebInterface()

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/newgame')
def newgame():
    # Note that in Python, objects and variables
    # in the global space are available to
    # top-level functions
    global game
    game = Board()
    game.start()
    global movehistory
    movehistory = MoveHistory(5)
    ui.board = game.display()
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = ""
    ui.btnlabel = 'Move'
    ui.action = "/play"
    return redirect(url_for('play'))
    # , _external=True, _scheme='https' (for https redirection)


@app.route('/play',methods=['POST', 'GET'])
def play():
    # TODO: get player move from GET request object
    # currently using post lol
    # if there is no player move, render the page template
    if request.method == 'POST':
        move = request.form['player_input']
        try:
            start, end = move.split(' ')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            movehistory.push([start,end,game.movetype(start,end),game.get_piece(end)])
            game.update(start, end)
            if game.promotepawns() == True:
                return redirect(url_for('promote'))
            else:
                game.next_turn()
                ui.board = game.display()
                ui.inputlabel = f'{game.turn} player: '
                ui.errmsg = ""
                return render_template('chess.html', ui=ui)
        except Exception as e:
            ui.errmsg = "Error: " + str(e)
            return render_template('chess.html', ui=ui)
    return render_template('chess.html', ui=ui)
    # Validate move, redirect player back to /play again if move is invalid
    # TODO: If move is valid, check for pawns to promote
    # TODO: Redirect to /promote if there are pawns to promote, otherwise


@app.route('/undo')
def undo():
    move = movehistory.pop()
    if move == None:
        ui.errmsg = "No moves to undo"
    else:
        game.undo(move)
        game.next_turn()
        ui.board = game.display()
        ui.inputlabel = f'{game.turn} player: '
    return redirect('/play')

@app.route('/promote',methods = ["POST", "GET"])
def promote():
    ui.board = game.display()
    ui.action = "/promote"
    ui.inputlabel = f"{game.turn} promote: "
    ui.errmsg = "Promote pawn to (r=Rook, k=Knight, b=Bishop, q=Queen)"
    if request.method == 'POST':
        promote = request.form['player_input']
        promotepiece = game.promoteprompt(promote)
        if promotepiece == False:
            pass
        game.promotepawns(promotepiece)
        game.next_turn()
        ui.board = game.display()
        ui.inputlabel = f'{game.turn} player: '
        ui.errmsg = ""
        ui.action = "/play"
        return render_template('chess.html', ui=ui)
    return render_template("chess.html", ui=ui)
    



app.run('0.0.0.0', debug=True)
