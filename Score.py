"""
Score.py
A package that is in charge of managing the scores file.
The scores file at this point will consist of only a number. That number is the accumulation of the
winnings of the user. Amount of points for winning a game is as follows:
POINTS_OF_WINNING = (DIFFICULTY X 3) + 5
Each time the user is winning a game, the points he one will be added to his current amount of
point saved in a file.
Methods
1. add_score - The function’s input is a variable called difficulty. The function will try to read
the current score in the scores file, if it fails it will create a new one and will use it to save
the current score.
"""

import os


def add_score(difficulty):

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file = os.path.join(script_dir, 'scores_file.txt')  # Store file in script's directory

    # Get the current working directory
    print(f"File should be located at: {os.path.abspath('scores_file.txt')}")

    # if score.txt file doesn't exist, then we will create one and put the number zero in it:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write('0')
    
    # Here we will add points if the player wins to the score.txt file:
    with open(file, 'r+') as f1:
        current_score = f1.read()
        print(f"Score BEFORE adding the new points: {current_score}")
        points_of_winning = (difficulty * 3) + 5

        current_score = int(current_score) + points_of_winning
        f1.seek(0) # Here the cursor goes back to the beginning of the file.
        f1.write(str(current_score))
        print(f"Score AFTER adding the new points: {current_score}")