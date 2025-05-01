# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import traceback

def automated_game_test(url):
    driver = None
    try:
        print("Launching browser...")

        options = webdriver.ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 120)

        print(f"Opening game: {url}")
        driver.get(url)

        # Step 1: Manually enter name and start game
        print("Please enter your name and click 'START PLAYING!' on the webpage.")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'START PLAYING!')]")))

        # Step 2: Wait for game to start
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "game-card")))
        print("Game selection loaded. Please proceed manually.")

        # Step 3: Wait for Finish button on result page
        print("Waiting for you to finish and click the 'Finish' button on the result page...")
        finish_button = wait.until(EC.element_to_be_clickable((By.ID, "finish-test-btn")))
        finish_button.click()

        print("Finish button clicked. Fetching result...")

        try:
            result_element = wait.until(EC.presence_of_element_located((By.ID, "resultMessage")))
        except:
            result_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "message")))

        result_text = result_element.text.strip()
        print(f"\nResult message: {result_text}")

        if "score" in result_text.lower():
            match = re.search(r"score\s*is\s*[:\-]?\s*(\d+)", result_text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                print(f"Extracted score: {score}")
                assert 1 <= score <= 1000, "Score out of expected range!"
        else:
            print("Game lost or no score detected.")

    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        traceback.print_exc()
        if driver:
            print("\nPage content at failure:")
            print(driver.page_source)
        raise
    finally:
        if driver:
            pass


if __name__ == "__main__":
    automated_game_test("http://localhost:8777")