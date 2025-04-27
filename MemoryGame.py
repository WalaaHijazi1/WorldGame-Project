"""
MemoryGame.py
The purpose of memory game is to display an amount of random numbers to the users for 0.7
seconds and then prompt them from the user for the numbers that he remember. If he was right
with all the numbers the user will win otherwise he will lose.
Properties
1. Difficulty

Methods
1. generate_sequence - Will generate a list of random numbers between 1 to 101. The list
length will be difficulty.
"""
import random
import time

def generate_sequence(difficulty_len):

    generated_list = random.sample(range(1,101),difficulty_len)

    print("Memorize this sequence: ", generated_list)
    time.sleep(1)  
    print("\n" * 100)

    return  generated_list

"""
3. is_list_equal - A function to compare two lists if they are equal. The function will return
True / False.
"""

def is_list_equal(list1,list2):

    return list1 == list2