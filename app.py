from flask import Flask, request, render_template,session,jsonify
from boggle import Boggle

# Start the server
app = Flask(__name__)
app.config['SECRET_KEY'] = "itisasecret"
# create a new instance of a class
boggle_game = Boggle()

@app.route("/")
def show_board():
    """Show board."""
    
    #.make_board() makes and returns a random boggle board.
    board=boggle_game.make_board() 
    #save the board to session
    session['board'] = board
    # get highscore from session, if not exsiting return defaul value 0
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    # render html and put the passed parameters dynamicly 
    return render_template("home.html",board=board,highscore=highscore, nplays=nplays)


# send request without using JS.
# @app.route("/check_guess" , methods=['GET', 'POST'])
# def check_guess():
#     """Check if the user guessed word is in dictionary."""
#     game_board=session["game_board"]
#     guessed_word=request.form.get("guessedword") 
#     result = boggle_game.check_valid_word(game_board,guessed_word )
#     return render_template("home.html",board=game_board,guessed_word=guessed_word,result=result)



@app.route("/checkword")
def check_word():
    """Check if word is in dictionary."""
    # get user input from the request sent through AJAX
    word = request.args['word']
    board=session["board"]
    # check word validity by using functions from boogle
    # .check_valid_world will check if a word is a valid word in the dictionary and/or the boggle board 
    # and return a string
    response = boggle_game.check_valid_word(board, word)
    # send back response
    return jsonify({'result': response})

@app.route("/postscore", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score."""
    #where does this "score" variable come from? why request.json?
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    # update number of plays
    session['nplays'] = nplays + 1
    # max() is used to find the largest item between two parameters.
    session['highscore'] = max(score, highscore)
    # brokeRecord stores a boolean value, true when a score is bigger than highscore
    return jsonify(brokeRecord=score > highscore)