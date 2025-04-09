"""
This game will use the free currency api to get the current exchange rate from USD to ILS, will
generate a new random number between 1-100 a will ask the user what he thinks is the value of
the generated number from USD to ILS, depending on the user’s difficulty his answer will be
correct if the guessed value is between the interval surrounding the correct answer

Properties
1. Difficulty
Methods
1. get_money_interval -Will get the current currency rate from USD to ILS and will
generate an interval as follows:
a. for given difficulty d, and total value of money t the interval will be: (t - (5 - d), t +
(5 - d))
"""

from currency_converter import CurrencyConverter
import requests
import json

def get_money_interval(user_input,d):
    c = CurrencyConverter()
    amount_ils = c.convert(user_input, 'USD', 'ILS')
    interval_min, interval_max = (amount_ils - (5 - d), amount_ils +(5 - d))
    return interval_max, interval_min

"""
2. get_guess_from_user - A method to prompt a guess from the user to enter a guess of
value to a given amount of USD
"""
def get_guess_from_user():

    try:
        user_input = float(input("Could you give me the amount in Dollars ($): "))
        return user_input
    except ValueError:
        print("Error! the program is asking for a number not a word!")
    except Exception as e:
        print("Unusual Error: ", e)

"""
3. play - Will call the functions above and play the game. Will return True / False if the user
lost or won.
"""

def play(difficulty):
    print(f"Game Difficulty Level: {difficulty}")

    user_input = get_guess_from_user()
    if user_input is None:
        return False

    interval_max, interval_min = get_money_interval(user_input, difficulty)
    if interval_min is None and interval_max is None:
        print("Could not retrieve exchange rate. Try again later.")
        return False

    # Get user's guess in ILS
    user_guess = float(input("Guess the value in ILS: "))

    if interval_min <= user_guess <= interval_max:
        print(f"Congratulations! Your guess {user_guess} ILS is within the interval ({interval_max},{interval_min})")
        return True
    else:
        print(f"Wrong guess! The correct value was within ({interval_max},{interval_min}), but you guessed {user_guess} ILS.")
        return False
