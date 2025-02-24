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
# options = Options()
# options.add_argument("--headless")  # Run browser in the background
# options.add_argument("--disable-gpu")
# options.add_argument("--window-size=1920,1080")

# Initialize WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def check_stock():
    driver.get(TARGET_PRODUCT_URL_TEST_STOCK)
    time.sleep(5)  # Allow time for JavaScript to load

    try:
        # Check if the "Add to Cart" button exists and is enabled
        add_to_cart_button = driver.find_element(By.XPATH, "//button[@id='addToCartButtonOrTextIdFor91351689']")
        
        if add_to_cart_button.is_enabled():
            add_to_cart_button.click()
            time.sleep(5)
            print("🚀 Product is IN STOCK!")
            return True
    except:
        pass

    try:
        # Check if the button has a "disabled" attribute (Out of Stock)
        disabled_button = driver.find_element(By.XPATH, "//button[@id='addToCartButtonOrTextIdFor88897904'][@disabled]")
        if disabled_button:
            print("❌ Product is OUT OF STOCK.")
            return False
    except:
        pass

    print("⚠️ Stock status unknown. Check manually.")
    return None

if __name__ == "__main__":
    check_stock()
    driver.quit()
