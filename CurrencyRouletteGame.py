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
import random

def get_money_interval(random_number1,d):
    c = CurrencyConverter()
    # converting the number from dollars to shekels
    amount_ils = c.convert(random_number1, 'USD', 'ILS')
    interval_min, interval_max = (amount_ils - (5 - d), amount_ils +(5 - d))
    return interval_max, interval_min

"""
2. get_guess_from_user - A method to prompt a guess from the user to enter a guess of
value to a given amount of USD
"""
def get_random_num():

    # Generate a random number from 1 to 100 using randint function.
    random_number = random.randint(1,100)

    return random_number