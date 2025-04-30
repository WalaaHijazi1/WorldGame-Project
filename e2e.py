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

#path = r"C:\Users\Smart\Downloads\chromedriver-win64\chromedriver.exe" # path to Chrome Driver.
#service = Service(path)
# driver = webdriver.Chrome(service=service)



def test_scores_service(url):

    driver = None


    try:
    
                # Setup WebDriver
        driver_options = Options()
        driver_options.add_argument('--headless')
        driver_options.add_argument('--no-sandbox')
        driver_options.add_argument('--disable-dev-shm-usage')
        
        service = Service()  # You can provide the path to chromedriver if needed
        driver = webdriver.Chrome(service=service, options=driver_options)
        
        # Go to the given URL
        print(f"Navigating to {url}")
        driver.get(url)

        # Wait up to 10 seconds for the score element to appear
        wait = WebDriverWait(driver, 10)
        score_element = wait.until(EC.presence_of_element_located((By.ID, "score")))

        # Extract score text and convert to int
        score_text = score_element.text.strip()
        print("Found score text:", score_text)
        score = int(score_text)

        # Check if score is within expected range
        if 1 < score < 1000:
            print("Test passed. Score is within expected range.")
            return True
        else:
            print("Test failed. Score is out of range.")
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


"""
2. main_function to call our tests function. The main function will return -1 as an OS exit
code if the tests failed and 0 if they passed.
"""
def main_function():
    url = "http://localhost:8777"
    result = test_scores_service(url)

    if result:
        print("Test has passed successfully...")
        sys.exit(0)

    else:
        print("Test Failed!")
        sys.exit(-1)


if __name__ == '__main__':
    main_function()
