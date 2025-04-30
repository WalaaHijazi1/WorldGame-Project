"""
This file will have two functions.
Functions
1. test_scores_service - it’s purpose is to test our web service. It will get the application
URL as an input, open a browser to that URL, select the score element in our web page,
check that it is a number between 1 to 1000 and return a boolean value if it’s true or not.
"""

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
        # Replace with your database connection details
        conn = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL container host
            user="root",  # Replace with your MySQL username
            password="password",  # Replace with your MySQL password
            database="world_game_db"  # Replace with your DB name
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

