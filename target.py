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

def create_driver():
    options = Options()
    options.add_argument("--headless")  # Run browser in the background
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="133.0.6943.127").install()))
    print("Chrome version:", driver.capabilities['browserVersion'])
    print("Chrome path:", driver.capabilities['chrome']['chromedriverVersion'])
    return driver

def check_stock():
    while True:
        # Create a new browser instance
        driver = create_driver()
        
        try:
            driver.get(TARGET_PRODUCT_URL)
            time.sleep(1)  # Allow time for JavaScript to load

            try:
                # Check if the "Add to Cart" button exists and is enabled
                add_to_cart_button = driver.find_element(By.XPATH, "//button[@id='addToCartButtonOrTextIdFor88897904']")
                
                if add_to_cart_button.is_enabled():
                    print("🚀 Product is IN STOCK! Clicking add to cart!")
                    add_to_cart_button.click()
                    time.sleep(1)
                    print("🚀 Product is IN STOCK!")
                    driver.quit()
                    return True
            except:
                pass

            try:
                # Check if the button has a "disabled" attribute (Out of Stock)
                disabled_button = driver.find_element(By.XPATH, "//button[@id='addToCartButtonOrTextIdFor88897904'][@disabled]")
                if disabled_button:
                    print("❌ Product is OUT OF STOCK. Retrying in 5 seconds...")
            except:
                print("⚠️ Stock status unknown. Retrying in 5 seconds...")

        finally:
            # Always close the browser
            driver.quit()
            time.sleep(5)  # Wait before next attempt

if __name__ == "__main__":
    check_stock()