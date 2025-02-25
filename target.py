from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time
import re

ua = UserAgent()

def extract_product_id(url: str) -> str:
    match = re.search(r'/A-(\d+)', url)
    return match.group(1) if match else None

TARGET_URLS = [
    "https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab",
    "https://www.target.com/p/pok-233-mon-trading-card-game-zapdos-ex-deluxe-battle-deck/-/A-91351689#lnk=sametab",
]
# in seconds
RETRY_TIMING = 5

def create_driver():
    options = Options()
    # options.add_argument("--headless")  # Run browser in the background
    
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="133.0.6943.127").install()), options=options)
    print("Chrome version:", driver.capabilities['browserVersion'])
    print("Chrome path:", driver.capabilities['chrome']['chromedriverVersion'])
    print("User Agent:", user_agent)
    return driver

def check_stock(url):
    # Create a new browser instance
    driver = create_driver()
    
    product_sku = extract_product_id(url)

    print(f"Checking stock for URL: {url}")
    print(f"Checking stock for SKU: {product_sku}")

    try:
        driver.get(url)
        time.sleep(1)

        try:
            addtocart_button = driver.find_element(By.XPATH, f"//button[@id='addToCartButtonOrTextIdFor{product_sku}']")
            if addtocart_button.is_enabled():
                print("🚀 Product is IN STOCK! Adding to cart...")
                addtocart_button.click()
                time.sleep(1)
            else:
                print("❌ Product is OUT OF STOCK. Retrying in 5 seconds...")
        except Exception as e:
            print("⚠️ Stock status unknown. Retrying in 5 seconds...")

    finally:
        driver.quit()
        time.sleep(RETRY_TIMING)

def main():
    while True:
        for url in TARGET_URLS:
            check_stock(url)
        print("Retrying all URLs in 5 seconds...\n")

if __name__ == "__main__":
    main()
