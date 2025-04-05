"""
         WORLD OF GAMES PROJECT
                                   """

import MemoryGame
import GuessGame
import CurrencyRouletteGame
import os
from Score import add_score

def welcome(name):
    print(f"Hello {name} and welcome to The World of Games (WoG).")
    print("Here you can find many cool games to play!")
    load_game()


"""
Function Update
Change the function load_game() as follows:
In case the user won the game, the function will call the function called add_score to add the
new score the user won to the score saved in the Scores.txt function.
"""

def game_difficulty_level():
    while True:
        try:
            game_difficulty = int(input("Please choose game difficulty from 1 to 5: "))
            if 1 <= game_difficulty <= 5:
                print(f"The game difficulty you chose is {game_difficulty}")
                return game_difficulty
            else:
                print("Invalid choice! Please enter a number between 1 and 5.")
        except ValueError:
            print("Error! You entered an invalid input. Please enter a number.")



def load_game():
    print("Please choose a game to play:")
    print("1.Memory Game - a sequence of numbers will appear for 1 second and you have to guess it back.")
    print("2.Guess Game - guess a number and see if you chose like the computer.")
    print("3.Currency Roulette - try and guess the value of a random amount of USD in ISL.")

    while True:
        try:
            game_choice = input("Which game do you want to choose? 1, 2 or 3?  ")
            game_choice = int(game_choice)

            if game_choice == 1:
                print("You picked number 1: Memory Game")
                difficulty = game_difficulty_level()
                game_result = MemoryGame.play(difficulty)

            elif game_choice == 2:
                print("You picked number 2: Guess Game")
                difficulty = game_difficulty_level()
                game_result = GuessGame.play(difficulty)

            elif game_choice == 3:
                print("You picked number 3: Currency Roulette")
                difficulty = game_difficulty_level()
                game_result = CurrencyRouletteGame.play(difficulty)

            else:
                print("Invalid choice! Please enter 1, 2, or 3.")           
            break
        except ValueError:
            print("Error! Invalid input. Please enter a number (1, 2, or 3).")

    if game_result:
        add_score(difficulty)
        print("Winning points has been added to your score. :)")
    else:
        print("You lost the game, zero points will be added to your SCORE!...")

if __name__=='__main__':
    welcome('Walaa')
