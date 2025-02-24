from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

TARGET_PRODUCT_URL = "https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab"

def create_driver():
    options = Options()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def check_stock():
    driver = create_driver()
    
    try:
        driver.get(TARGET_PRODUCT_URL)
        time.sleep(1)  # Allow JavaScript to load

        try:
            add_to_cart_button = driver.find_element(By.XPATH, "//button[@id='addToCartButtonOrTextIdFor88897904']")
            if add_to_cart_button.is_enabled():
                print("🚀 Product is IN STOCK!")
                return True
        except:
            pass

        try:
            disabled_button = driver.find_element(By.XPATH, "//button[@id='addToCartButtonOrTextIdFor88897904'][@disabled]")
            if disabled_button:
                print("❌ Product is OUT OF STOCK.")
                return False
        except:
            print("⚠️ Stock status unknown.")

    finally:
        driver.quit()

    return False  # Default to out of stock if unsure