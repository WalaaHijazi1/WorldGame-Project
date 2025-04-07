from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")

def test_scores_service(url):
    max_retries = 3
    for attempt in range(max_retries):
        driver = None
        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), 
                options=options
            )
            driver.set_page_load_timeout(30)
            driver.get(url)
            
            time.sleep(2)
            score_element = driver.find_element(By.ID, 'score')
            score = int(score_element.text.strip())
            
            if 1 <= score <= 1000:
                return True
            else:
                print(f"Score {score} out of range!")
                return False
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                print("All retries exhausted!")
                return False
            time.sleep(5)
        finally:
            if driver:
                driver.quit()

def main_function():
    # Use environment variable or default to localhost
    url = "http://localhost:8777"  # ✅ Use correct URL for your environment
    if test_scores_service(url):
        print("Test passed!")
        sys.exit(0)
    else:
        print("Test failed!")
        sys.exit(-1)

if __name__ == '__main__':
    main_function()