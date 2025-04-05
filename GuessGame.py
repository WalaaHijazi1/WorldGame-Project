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
    secret_number = random.randint(1,difficulty)
    return secret_number


"""
2. get_guess_from_user - Will prompt the user for a number between 1 to difficulty and
return the number.
"""

def get_guess_from_user(difficulty):
    try:
        user_choice =  int(input("Guess the maximum number of difficulty of the game? "))

        if 1 <= user_choice <= difficulty:
            return user_choice
        else:
            print(f"Error! Please enter a number between 1 and {difficulty}.")
            return get_guess_from_user(difficulty)

    except ValueError:
        print("Error! the program is asking for a integer not a word!")

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

"""
4. play - Will call the functions above and play the game. Will return True / False if the user
lost or won.
"""
def play(difficulty):
    """
    Main game function. Asks the user for a difficulty level, generates a secret number, and
    checks the user's guess.
    """
    try:
        if difficulty < 1 or difficulty > 100:
            print("Please enter a number between 1 and 100.")
            return play()  # Restart the game
        
        # Generate the secret number in another func:
        secret_number = generate_number(difficulty)

        # Get a guessed number from the user:
        user_guess = get_guess_from_user(difficulty)

        # Compare the secret number that was generated and the number that was guessed by the user:
        # if both numbers are equal then the player wins the game, but if not he loses! 
        result = compare_results(user_guess, secret_number)


        if result:
            print("Congratulations! You won!")
            return True
        else:
            print("Sorry, you lost.")
            return False

    except ValueError:
        print("Invalid input. Please enter a number.")
        return play()  # Restart if input is invalid
