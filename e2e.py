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
        driver_options = Options()
        driver_options.add_argument('--headless')
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())  # Path to chromedriver if necessary
        driver = webdriver.Chrome(service=service, options=driver_options)
        
        # Navigate to the homepage of the game
        print(f"Navigating to {url}")
        driver.get(url)

        # Wait for the homepage elements (like the form to enter name) to load
        time.sleep(2)  # A small wait for the page to load
        
        # Find the input box and button, then interact with them
        name_input = driver.find_element(By.NAME, "Name")
        start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'START PLAYING!')]")
        
        # Input a name and click start
        name_input.send_keys("Test Player")
        start_button.click()

        # Wait for the game result (after starting the game, waiting for the result page)
        time.sleep(5)  # Wait for the game to process

        # Find the result page to determine if the user won or lost
        try:
            result_message = driver.find_element(By.ID, "resultMessage").text
            print("Result Message:", result_message)
        except Exception as e:
            print("Error retrieving result message:", e)
            result_message = "Error"
        
        # If the player won
        if "won" in result_message.lower():
            print("Player has won!")
            status = "won"
        elif "lost" in result_message.lower():
            print("Player has lost!")
            status = "lost"
        else:
            print("Could not determine the result of the game.")
            status = "error"

        # Fetch score from the database if player won or lost
        score = get_score_from_db()

        # Return the result based on the status
        if status == "won":
            print(f"Test passed. Player won. Score from DB: {score}")
            return True
        elif status == "lost":
            print(f"Test failed. Player lost. Score from DB: {score}")
            return False
        else:
            print(f"Test failed. Could not determine result. Score from DB: {score}")
            return False

    except Exception as e:
        print("Test failed with exception:", e)
        if driver:
            print("Page source for debugging:")
            print(driver.page_source)
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

