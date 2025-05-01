# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import traceback

def automated_game_test(url):
    driver = None
    try:
        print("Launching browser...")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # crucial for CI/CD
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 40)

        print(f"Opening game: {url}")
        driver.get(url)

        # Step 1: Fill name and click start
        wait.until(EC.presence_of_element_located((By.NAME, "Name"))).send_keys("AutoTester")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'START PLAYING!')]"))).click()

        # Step 2: Choose a game
        game = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".game-card")))
        game.click()

        # Step 3: Choose difficulty
        difficulty = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".difficulty-option[data-difficulty='1']")))
        difficulty.click()

        # Step 4: Start game
        wait.until(EC.element_to_be_clickable((By.ID, "startBtn"))).click()
        

        time.sleep(25)  # wait for manual play and submission


        # Step 5: Wait for result element
        print("Waiting for result message...")
        try:
            result_element = wait.until(EC.presence_of_element_located((By.ID, "resultMessage")))
        except:
            result_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "message")))

        result_text = result_element.text.strip()
        print(f"\nResult message: {result_text}")

        # Step 6: Extract score
        match = re.search(r"score\s*is\s*[:\-]?\s*(\d+)", result_text, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            print(f"Extracted score: {score}")
            assert 1 <= score <= 1000, "Score is out of expected range!"
        else:
            print("Score not found. Possibly a loss or format issue.")

    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        traceback.print_exc()
        # Optional: Dump page content for debugging
        if driver:
            print("\nPage content at failure:")
            print(driver.page_source)
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    automated_game_test("http://localhost:8777")












































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
                driver.find_element(By.ID, "startBtn").click()
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
                    print(f"✅ Valid score from DB: {score}")
                else:
                    print(f"❌ Invalid score from DB: {score}")
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
        print("\nAll tests passed successfully!")
        sys.exit(0)
    else:
        print("\n❌ One or more tests failed.")
        sys.exit(1)


if __name__ == '__main__':
    main_function()

######################################################################################################

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
                    print(f"✅ {game_id} passed.")
                else:
                    print(f"❌ {game_id} lost (but continuing).")

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