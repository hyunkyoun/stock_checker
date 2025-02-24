from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Target Product Page
TARGET_PRODUCT_URL = "https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab"
TARGET_PRODUCT_URL_TEST_STOCK = "https://www.target.com/p/pok-233-mon-trading-card-game-zapdos-ex-deluxe-battle-deck/-/A-91351689#lnk=sametab"

# Set up Selenium options
options = Options()
options.add_argument("--headless")  # Run browser in the background
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def check_stock():
    driver.get(TARGET_PRODUCT_URL_TEST_STOCK)
    time.sleep(5)  # Allow time for JavaScript to load
    
    # Save the full page source
    page_source = driver.page_source

    with open("target_page_instock.html", "w", encoding="utf-8") as file:
        file.write(page_source)

    # # Check for "Add to Cart" button
    # try:
    #     add_to_cart = driver.find_element(By.XPATH, "//button[contains(text(), 'Add to cart')]")
    #     if add_to_cart.is_displayed():
    #         print("🚀 Product is in stock!")
    #         return True
    # except:
    #     pass

    # # Check for "Sold Out" message
    # try:
    #     sold_out = driver.find_element(By.XPATH, "//div[contains(text(), 'Sold out')]")
    #     if sold_out.is_displayed():
    #         print("❌ Product is out of stock.")
    #         return False
    # except:
    #     pass

    print("⚠️ Stock status unknown. Check manually.")
    return None

if __name__ == "__main__":
    check_stock()
    driver.quit()
