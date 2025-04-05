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
from GuessGame import generate_number
import random
import time

def generate_sequence(difficulty_len):

    generated_list = random.sample(range(1,101),difficulty_len)

    print("Memorize this sequence: ", generated_list)
    time.sleep(10)  # Show numbers for 0.7 seconds
    print("\n" * 100)

    return  generated_list


"""
2. get_list_from_user - Will return a list of numbers prompted from the user. The list length
will be in the size of difficulty.
"""

def get_list_from_user(list_len):
    final_num_lst = []
    print(f"Enter {list_len} numbers you remember:")

    for i in range(list_len):
        while True:
            try:
                num = int(input(f"Enter number {i + 1}: "))
                final_num_lst.append(num)
                break  # Break out of retry loop once a valid number is entered
            except ValueError:
                print("Invalid input! Please enter an integer.")

    return final_num_lst
"""
3. is_list_equal - A function to compare two lists if they are equal. The function will return
True / False.
"""

def is_list_equal(list1,list2):

    return list1 == list2

"""
4. play - Will call the functions above and play the game. Will return True / False if the user
lost or won.
"""

def play(difficulty):

    # difficulty = int(input("Choose a difficulty level (1-10): "))  # Difficulty defines the list length
    sequence_to_remember = generate_sequence(difficulty)

    user_list = get_list_from_user(difficulty)

    if is_list_equal(sequence_to_remember, user_list):
        print("Congratulations! You won!")
        return True
    else:
        print(f"Sorry, you lost. The correct sequence was: {sequence_to_remember}")
        return False
