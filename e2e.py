from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys

def test_scores_service(app_url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Use ChromeDriverManager or ensure chromedriver is in PATH
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options
        )
        driver.get(app_url)
        
        score_element = driver.find_element(By.ID, 'score')
        score = int(score_element.text)
        return 1 <= score <= 1000
    except Exception as e:
        print(f"Error during test: {e}")
        return False
    finally:
        driver.quit()

def main_function():
    app_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8777'
    result = test_scores_service(app_url)
    sys.exit(0 if result else -1)

if __name__ == "__main__":
    main_function()