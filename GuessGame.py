"""
GuessGame.py
The purpose of guess game is to start a new game, cast a random number between 1 to a
variable called difficulty. The game will get a number input from the
Properties
1. Difficulty
2. Secret number

Methods
1. generate_number - Will generate number between 1 to difficulty and save it to
secret_number.
"""

import random

def generate_number(difficulty):
    # The random.randint is a function that generates a number from 1 to difficulty,
    # difficulty a number that is chosen by the player.
    secret_number = random.randint(1,difficulty)
    return secret_number


"""
3. compare_results - Will compare the the secret generated number to the one prompted
by the get_guess_from_user.
"""

def compare_results(user_num,game_num):
    if user_num == game_num:
        print("True, you guessed the right number!")

        return True

    else:
        print("False, You gave the wrong number")
        return False