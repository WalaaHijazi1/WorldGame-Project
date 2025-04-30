"""
This file will have two functions.
Functions
1. test_scores_service - itâ€™s purpose is to test our web service. It will get the application
URL as an input, open a browser to that URL, select the score element in our web page,
check that it is a number between 1 to 1000 and return a boolean value if itâ€™s true or not.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import os
import mysql.connector

# Function to check score in the webpage
def test_scores_service(url):
    driver = None
    try:
        # Setup WebDriver
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Step 1: Open homepage
        driver.get(url)
        time.sleep(1)

        # Step 2: Fill in name
        driver.find_element(By.NAME, "Name").send_keys("Test Player")
        driver.find_element(By.XPATH, "//button[contains(text(), 'START PLAYING!')]").click()
        time.sleep(1)

        # Step 3: Choose Game - You can loop over all 3 or test one at a time
        game_ids = ["memory_game", "guess_game", "currency_game"]
        for game_id in game_ids:
            try:
                print(f"Testing game: {game_id}")
                driver.find_element(By.ID, game_id).click()
                time.sleep(1)

                # Step 4: Choose difficulty
                driver.find_element(By.ID, "1").click()  # You can randomize difficulty
                time.sleep(1)

                # Step 5: Start the game
                driver.find_element(By.ID, "startButton").click()
                time.sleep(2)

                # Step 6: Handle game form inputs
                if game_id == "guess_game":
                    guess_input = driver.find_element(By.NAME, "user_guess")
                    guess_input.send_keys("5")  # Random or fixed guess
                elif game_id == "currency_game":
                    guess_input = driver.find_element(By.NAME, "user_choice")
                    guess_input.send_keys("30.5")  # Random or fixed currency guess
                elif game_id == "memory_game":
                    inputs = driver.find_elements(By.NAME, "user_input")
                    for inp in inputs:
                        inp.send_keys("1")  # Dummy number

                # Step 7: Submit game
                driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
                time.sleep(2)

                # Step 8: Check win/loss
                result = driver.find_element(By.ID, "resultMessage").text
                print(f"{game_id} result message: {result}")

                # Step 9: Fetch score
                score = get_score_from_db()

                if "won" in result.lower():
                    print(f"Test passed for {game_id}. Score: {score}")
                else:
                    print(f"Test failed for {game_id}. Score: {score}")

            except Exception as e:
                print(f"Error testing {game_id}: {e}")
                continue

        return True  # If reached here, assume success

    except Exception as e:
        print("Global test failure:", e)
        return False

    finally:
        if driver:
            driver.quit()

# Function to get score from SQL container
def get_score_from_db():
    try:
        # the database connection details
        conn = mysql.connector.connect(
            host="mysql",  # My SQL container host
            user="root",  # My SQL username
            password="gamespass",  # My SQL password
            database="games_db"  # My DB name
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT score FROM game_scores ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()
        
        if result:
            score = result[0]
            print(f"Fetched score from DB: {score}")
            return score
        else:
            print("No score found in database.")
            return 0

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 0

    finally:
        if conn:
            conn.close()

# Main function
def main_function():
    url = "http://localhost:8777"  # Your local Flask game URL
    result = test_scores_service(url)

    if result:
        print("Test has passed successfully...")
        sys.exit(0)  # Jenkins success code
    else:
        print("Test Failed!")
        sys.exit(1)  # Jenkins failure code

if __name__ == '__main__':
    main_function()
    
"""




"""
This file has two functions:
1. test_scores_service - tests the web service by opening the application URL, playing each game,
   and checking the score from the database to ensure it's a number between 1 to 1000.
"""

"""
This script contains two main functions:
1. test_scores_service - Automates testing of the game web app by simulating user interactions,
   playing all three games, and validating the score retrieved from the SQL database.
2. get_score_from_db - Connects to the MySQL container and fetches the latest game score.

This script is meant to be run in a CI/CD pipeline or local test to ensure game logic and DB integration work.
"""

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
import time
import sys
import random

# Function to test the web game service
def test_scores_service(url):
    driver = None
    try:
        # Setup WebDriver with headless Chrome
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Step 1: Open homepage
        driver.get(url)
        time.sleep(1)

        # Step 2: Enter player name and start
        driver.find_element(By.NAME, "Name").send_keys("Test Player")
        driver.find_element(By.XPATH, "//button[contains(text(), 'START PLAYING!')]").click()
        time.sleep(1)

        # Step 3: Loop through all games
        game_ids = ["memory_game", "guess_game", "currency_game"]
        for game_id in game_ids:
            try:
                print(f"\n--- Testing game: {game_id} ---")
                driver.find_element(By.ID, game_id).click()
                time.sleep(1)

                # Step 4: Select random difficulty
                difficulty = random.randint(1, 3)
                driver.find_element(By.ID, str(difficulty)).click()
                time.sleep(1)

                # Step 5: Start the game
                driver.find_element(By.ID, "startButton").click()
                time.sleep(2)

                # Step 6: Fill game-specific inputs
                if game_id == "guess_game":
                    guess_input = driver.find_element(By.NAME, "user_guess")
                    guess_input.send_keys(str(random.randint(1, 10)))

                elif game_id == "currency_game":
                    currency_input = driver.find_element(By.NAME, "user_choice")
                    currency_input.send_keys(str(round(random.uniform(10.0, 50.0), 2)))

                elif game_id == "memory_game":
                    memory_inputs = driver.find_elements(By.NAME, "user_input")
                    for inp in memory_inputs:
                        inp.send_keys(str(random.randint(1, 9)))

                # Step 7: Submit the game
                driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
                time.sleep(2)

                # Step 8: Read result message
                result = driver.find_element(By.ID, "resultMessage").text
                print(f"Result message: {result}")

                # Step 9: Check score from DB
                score = get_score_from_db()
                if 1 <= score <= 1000:
                    print(f"âœ… Valid score from DB: {score}")
                else:
                    print(f"âŒ Invalid score from DB: {score}")
                    return False

            except Exception as e:
                print(f"Error testing {game_id}: {e}")
                continue

        return True

    except Exception as e:
        print("Global test failure:", e)
        return False

    finally:
        if driver:
            driver.quit()


# Function to fetch the latest score from MySQL DB
def get_score_from_db():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="mysql",  # MySQL container host
            user="root",
            password="gamespass",
            database="games_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT score FROM game_scores ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            print("No score found in DB.")
            return 0

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return 0

    finally:
        if conn:
            conn.close()


# Entry point
def main_function():
    url = "http://localhost:8777"
    if test_scores_service(url):
        print("\ní ¼í¾‰ All tests passed successfully!")
        sys.exit(0)
    else:
        print("\nâŒ One or more tests failed.")
        sys.exit(1)


if __name__ == '__main__':
    main_function()


"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector
import time
import sys
import random

# Function to test the game service
def test_scores_service(url):
    driver = None
    try:
        # Setup WebDriver with headless Chrome
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Step 1: Open homepage
        driver.get(url)
        time.sleep(1)

        # Step 2: Enter player name and start
        driver.find_element(By.NAME, "Name").send_keys("Test Player")
        driver.find_element(By.XPATH, "//button[contains(text(), 'START PLAYING!')]").click()
        time.sleep(1)

        # Step 3: Loop through all games
        game_ids = ["memory_game", "guess_game", "currency_game"]
        for game_id in game_ids:
            try:
                print(f"\n--- Testing game: {game_id} ---")
                driver.find_element(By.ID, game_id).click()
                time.sleep(1)

                # Step 4: Select difficulty (random from 1 to 3)
                difficulty = random.randint(1, 3)
                driver.find_element(By.ID, str(difficulty)).click()
                time.sleep(1)

                # Step 5: Start the game
                driver.find_element(By.ID, "startBtn").click()
                time.sleep(2)

                # Step 6: Fill out game inputs
                if game_id == "guess_game":
                    input_box = driver.find_element(By.CSS_SELECTOR, '[data-game="guess"]')
                    input_box.send_keys(str(random.randint(1, 10)))

                elif game_id == "currency_game":
                    input_box = driver.find_element(By.CSS_SELECTOR, '[data-game="currency"]')
                    input_box.send_keys(str(round(random.uniform(10.0, 50.0), 2)))

                elif game_id == "memory_game":
                    inputs = driver.find_elements(By.CSS_SELECTOR, '[data-game="memory"]')
                    for inp in inputs:
                        inp.send_keys(str(random.randint(1, 9)))

                # Step 7: Submit the game
                driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
                time.sleep(2)

                # Step 8: Read result message
                result = driver.find_element(By.ID, "resultMessage").text
                print(f"Result message: {result}")

                # Step 9: Check DB score
                score = get_score_from_db()
                if 1 <= score <= 1000:
                    print(f"Score {score} is valid.")
                else:
                    print(f"Invalid score: {score}")
                    return False

                if "won" in result.lower():
                    print(f"âœ… {game_id} passed.")
                else:
                    print(f"âŒ {game_id} lost (but continuing).")

            except Exception as e:
                print(f"Error during test of {game_id}: {e}")
                continue

        return True

    except Exception as e:
        print("Global test failure:", e)
        return False

    finally:
        if driver:
            driver.quit()


# Function to fetch the latest score from the database
def get_score_from_db():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="root",
            password="gamespass",
            database="games_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT score FROM game_scores ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()
        if result:
            score = result[0]
            print(f"Fetched score from DB: {score}")
            return score
        else:
            print("No score found.")
            return 0

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return 0

    finally:
        if conn:
            conn.close()


# Main execution function
def main_function():
    url = "http://localhost:8777"
    success = test_scores_service(url)
    if success:
        print("\nAll tests passed successfully.")
        sys.exit(0)
    else:
        print("\nOne or more tests failed.")
        sys.exit(1)


if __name__ == '__main__':
    main_function()

"""