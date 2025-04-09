from Live import welcome , load_game


from GuessGame import play as play_guess_game
from MemoryGame import play as play_memory_game
from CurrencyRouletteGame import play as play_currency_game

def welcome(name):
    return f"Hello {name} and welcome to the World of Games (WoG)!"

def load_game():
    """
    Asks the user to choose a game and difficulty level, then starts the selected game.
    """
    print("Please choose a game to play:")
    print("1. Memory Game - a sequence of numbers will appear for 0.7 seconds and you have to guess it back")
    print("2. Guess Game - guess a number and see if you chose like the computer")
    print("3. Currency Roulette - try and guess the value of a random amount of USD in ILS")

    # Get the game selection from the user
    while True:
        try:
            game_choice = int(input("Enter the game number (1-3): "))
            if 1 <= game_choice <= 3:
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    # Get the difficulty level
    while True:
        try:
            difficulty = int(input("Choose a difficulty level (1-5): "))
            if 1 <= difficulty <= 5:
                break
            else:
                print("Invalid difficulty! Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    # Start the selected game with the given difficulty
    if game_choice == 1:
        print("\nStarting Memory Game...\n")
        play_memory_game(difficulty)
    elif game_choice == 2:
        print("\nStarting Guess Game...\n")
        play_guess_game(difficulty)
    elif game_choice == 3:
        print("\nStarting Currency Roulette Game...\n")
        play_currency_game(difficulty)


# Run the game only when executing this script directly
if __name__ == "__main__":
    print(welcome("Guy"))
    load_game()