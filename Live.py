"""
         WORLD OF GAMES PROJECT
                                   """
import MemoryGame
import GuessGame
import CurrencyRouletteGame
import os
from Score import add_score
from flask import Flask, render_template, request, redirect, url_for, session

# Creating an instance of a flask and passing a flask constructor:
app = Flask(__name__)
app.secret_key = 'something_secret_and_random'

# Creating an index route to the home page using a decorator:
@app.route('/')
def home():
    return render_template('homepage.html')  # The home page of the games where the name is has to be put.

"""
GET and POST are two HTTP methods, 
GET is a method to retrieve information/data from a server.
POST is a method to send data by the user to a server.
"""
# Redirect the player to the games page in order to choose, in a POST method:
@app.route('/start', methods=['POST'])
def start_game():    # Define the function for the specific route.
    # get the input name of the user, and save it in a 'name' variable.
    name = request.form.get('Name')
    if name:
        # session is used to store informations, across different requests, as interaction happens with the web app.
        # Here the player name - 'name' is saved in 'player_name' which is a variable that can be used in other url requests.
        session['player_name'] = name
        # Redirecting to the choose game function in the ChooseGame url route.
        return redirect(url_for('choose_game')) 
    else:
        return "Please enter your name!"


# Route to the ChooseGame page:
@app.route('/ChooseGame')
def choose_game():
    # retrieve the value stored under the key 'player_name' from the session,
    # if name doesn't exist 'Player' will be a default value of 'player_name'.
    name = session.get('player_name', 'Player')
    # render_template is a flask function renders html web pages and pass them to the browser.
    # All the html files MUST be in 'templates' that exists in the same directory of the python code file.
    # Here the user_name variable is passed to the 'ChooseGame.html' page
    return render_template('ChooseGame.html', user_name=name)


# Route to play_game, passing it to the dectator, the methods are in order to define client-server communication.
@app.route('/play_game', methods=['GET'])
def play_game():

    # request.args.get: is to get the game parameter using request arguments.
    # While - request.args contains query parameters from the URL (the part after the ? in a link).
    game = request.args.get('game')
    
    # Next, it will pull the difficulty parameter from the URL.
    # if the difficulty parameter doesn't exist the default value is 1.
    difficulty = int(request.args.get('difficulty', 1))

    if game == 'memory':
    
        # here the generate_sequence function is used from MemoryGame.py code.
        # it saves a sequence in the sequence variable, based on the difficulty that the player chose.
        sequence = MemoryGame.generate_sequence(difficulty)

        # here the sequence is saved under 'sequence' in session to be used in future requests.
        session['sequence'] = sequence
        
        # if the game is memory it will redirect it to the memory url web game page,
        # and passes the 'difficulty' and 'sequence' as variables to the html page.
        return render_template('MemoryGame.html', difficulty=difficulty, sequence=sequence)
    
    # Same goes if the game were guess or currency!
    elif game == 'guess':
    
        # generating a number using the function in GuessGame.py code file.
        secret_number = GuessGame.generate_number(difficulty)
        
        # Saving secret_number and difficulty in session to use in future requests.
        session['secret_number'] = secret_number
        session['difficulty'] = difficulty
        
        # if the game is guess it will redirect it to the guess url web game page,
        # and passes the 'difficulty' variable to the html page.
        return render_template('GuessGame.html', difficulty=difficulty)
        
    elif game == 'currency':
    
        session['difficulty'] = difficulty
        
        # using get_random_num() from CurrencyRouletteGame.py code 
        # the get_random_num function returns a random number from 1 to 100, and save it in random_num.
        random_num = CurrencyRouletteGame.get_random_num()
        session['random_num'] = random_num
        
        # passing the 'difficulty' and 'random_num' variables to the html page.
        return render_template('CurrencyRoulleteGame.html', difficulty=difficulty, random_num = random_num)
        
    else:
    
        # If the requested game is not found, the server responds with a 404 Not Found error.
        return "Game not found", 404

# Defining a route (/memory_result) that accepts POST requests, which send data from the client (browser) to the server.
@app.route("/memory_result", methods=['POST'])

def get_memory_results():

    # pulling the difficulty variable from the url.
    difficulty = int(request.form.get('difficulty'))
    
    # Takes a list of numbers the user submitted, turns them from strings into integers, and stores them in user_list.
    # map is a function that takes each user input and applies the int function on it.
    user_list = list(map(int, request.form.getlist('user_input')))
    
    # Retrieving the generated sequence (created by the server) that was previously saved under the 'sequence' key in the session.
    generated_list = session.get('sequence')
    
    # retrieve the value stored under the key 'player_name' from the session,
    # if name doesn't exist 'Player' will be a default value of 'player_name'.    
    name = session.get('player_name', 'Player')

    # is_list_equal is a func that compares the list inserted by the user and the genrated list by the game.
    # if both lists are equal then it will render the winner template.
    # the Winner.html template has a winning message to the player with it's name and the final score.
    if MemoryGame.is_list_equal(generated_list, user_list):
    
        current_score = add_score(difficulty,name)
        return render_template('Winner.html', current_score=current_score, user_name=name, message="You remembered the right sequence!")
        
    # if the two lists are not equal it will render the Lost.html web page that will tell the player that he has lost.
    else:
    
        return render_template('Lost.html', user_name=name, message="You missed the sequence.")

# Defining a route (/guess_result) that accepts POST requests, which send data from the client (browser) to the server.
@app.route('/guess_result', methods=['POST'])

def get_guess_results():

    # pulling the difficulty and user_guess variables from the url.
    difficulty = int(request.form.get('difficulty'))
    user_guess = int(request.form.get('user_guess'))

    # retrieve the value stored under the key 'player_name' from the session,
    # if name doesn't exist 'Player' will be a default value of 'player_name'.    
    name = session.get('player_name', 'Player')

    # secret_number is generated using generate_number function from GuessGame.py code.
    secret_number = GuessGame.generate_number(difficulty)

    # saving the secret number in session to use in future requests.
    session['secret_number'] = secret_number

    # if the user guess equals to secret number that generated by the game, so its a win
    # and the score will be added to the final score based on difficulty that was chosen
    if GuessGame.compare_results(user_guess,secret_number):
        current_score = add_score(difficulty,name)
        
        return render_template('Winner.html', current_score=current_score, user_name=name, message="You guessed the right number!")
        
    else:
        return render_template('Lost.html', user_name=name, message="You gave the wrong number.")

# Defining a route (/CurrencyRoulette_results) that accepts POST requests, which send data from the client (browser) to the server.
@app.route('/CurrencyRoulette_results', methods=['POST'])

def get_currencyroullette_results():

    # pulling the difficulty and turns it into integer, and user_choice and turns it into float number variables from the url.
    difficulty = int(request.form.get('difficulty'))
    user_choice = float(request.form.get('user_choice'))

    # Retrieving the random num that was previously saved under the 'random_num' key in the session.
    random_num = session.get('random_num')

    # passing the random_num and difficulty, then it returns the max and the min of 
    # the interval that is created by the get_money_interval function in CurrencyReletteGame.py code.
    max_interval, min_interval  = CurrencyRouletteGame.get_money_interval(random_num,difficulty)

    name = session.get('player_name', 'Player')

    # if the user choice is in the interval then the player wins, if not he loses.
    if min_interval <= user_choice <= max_interval:
        current_score = add_score(difficulty,name)
        
        return render_template('Winner.html', current_score=current_score, user_name=name, message="You guessed the right number!")
        
    else:
        return render_template('Lost.html', user_name=name, message="You gave the wrong number.")


if __name__=='__main__':

    # debug=True : that means that if we have any error in the webpage we can see.
    app.run(host='0.0.0.0',port=8777, debug=True)