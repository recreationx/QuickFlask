from flask import Flask
from flask import render_template, redirect, url_for, request
from chess import WebInterface, Board

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
    ui.board = game.display()
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = ""
    ui.btnlabel = 'Move'
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
            game.update(start, end)
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


@app.route('/promote')
def promote():
    pass


app.run('0.0.0.0', debug=True)
