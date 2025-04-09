# -*- coding: utf-8 -*-

#This file will have two functions.
#Functions
#1. test_scores_service - it’s purpose is to test our web service. It will get the application
#URL as an input, open a browser to that URL, select the score element in our web page,
#check that it is a number between 1 to 1000 and return a boolean value if it’s true or not.




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys

import os
import requests



def test_scores_service(url):
    options = Options()

    # Set Chrome options
    # Options available in Selenium that help in testing in the background, disabling extensions, etc.
    # It's an object that let the web driver customize the behavior of a web browser.
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-data-dir={os.path.expanduser('~')}/chrome_data")
    options.add_argument("--remote-debugging-port=9222")


    # Set up the ChromeDriver Service
    chromedriver_path = "/root/.wdm/drivers/chromedriver/linux64/134.0.6998.88/chromedriver-linux64/chromedriver"
    service = Service(executable_path=chromedriver_path)

    # Initialize the Chrome WebDriver with the service and options
    driver = webdriver.Chrome(service=service, options=options)



    try:

        driver.get(url)

        # Wait for the page to load
        time.sleep(2)
        
        # Explicitly wait for the score element to be visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'score')))

        #Find the score element:
        score_element = driver.find_element(By.ID, 'score')
        score_text = score_element.text.strip()

        # Check if score is in the wanted range:
        print("Found the score: ", score_text)

        score = int(score_text)

        # Check if score is in the wanted range:
        if 1 < score < 1000:
            return True
        else:
            return False
    except Exception as e:
        print("Test failed:", e)
        return False

    finally:
        if driver:
            driver.quit()




def wait_for_server(url, timeout=30):
    for _ in range(timeout):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print(f"Server is up: {url}")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    print("Server did not start in time")
    return False



#2. main_function to call our tests function. The main function will return -1 as an OS exit
#code if the tests failed and 0 if they passed.

def main_function():
    url = "http://localhost:8777"
    if wait_for_server("http://localhost:8777"):
      test_scores_service("http://localhost:8777")
      
    else:
      print("Flask server not reachable")
      exit(1)
    
    result = test_scores_service(url)

    if result:
        print("Test has passed successfully...")
        sys.exit(0)

    else:
        print("Test Failed!")
        sys.exit(-1)


if __name__ == '__main__':
    main_function()