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


    driver_options = Options()
    driver_options.add_argument("--headless")
    driver_options.add_argument("--no-sandbox")
    driver_options.add_argument("--disable-dev-shm-usage")
    driver_options.add_argument("--disable-gpu")
    #driver_options.binary_location = "/usr/bin/chromium"

    #chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/lib/chromium/chromedriver")
    #service = Service(executable_path=chromedriver_path)
    
    service = Service(ChromeDriverManager().install())


    #driver_options = Options()
    #driver_options.add_argument("--headless=new")
    #driver_options.add_argument("--no-sandbox")
    #driver_options.add_argument("--disable-dev-shm-usage")
    #driver_options.add_argument("--disable-gpu")
    #driver_options.add_argument("--remote-debugging-port=9222")

    # Correct ChromeDriver path for Debian
    #service = Service(ChromeDriverManager().install())
    #chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/lib/chromium/chromedriver")
    #service = Service(executable_path=chromedriver_path)

    


    #driver_options = Options()
    #driver_options.add_argument("--headless")
    #driver_options.add_argument("--no-sandbox")
    #driver_options.add_argument("--disable-dev-shm-usage")
    
    # Using system-installed ChromeDriver
    #service = Service("/usr/bin/chromedriver")
    
    #driver = webdriver.Chrome(service=service, options=driver_options)
    
    #####################################

    #driver_options = Options()

    #driver_options.add_argument("--headless=new")
    #driver_options.add_argument("--no-sandbox")
    #driver_options.add_argument("--disable-dev-shm-usage")
    
    
    # Set up the ChromeDriver Service
    #service = Service(ChromeDriverManager().install())
    # Set up the ChromeDriver Service
    #chromedriver_path = "/root/.wdm/drivers/chromedriver/linux64/134.0.6998.88/chromedriver-linux64/chromedriver"
    #service = Service(executable_path=chromedriver_path)
    
    # Initialize the Chrome WebDriver with the service and options
    #driver = webdriver.Chrome(service=service, options=driver_options)


    #driver.get(url)

    try:
        
        driver = webdriver.Chrome(service=service, options=driver_options)
        driver.get(url)


        # Wait for the page to load
        time.sleep(2)

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
