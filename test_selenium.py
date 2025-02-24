from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium options
# options = Options()
# options.add_argument("--headless")  # Run browser in the background
# options.add_argument("--disable-gpu")
# options.add_argument("--window-size=1920,1080")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://google.com")

input = driver.find_element(By.CLASS_NAME, "gLFyf")
input.send_keys("Hello, World!")

time.sleep(10)