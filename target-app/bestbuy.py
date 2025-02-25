# import requests
# from bs4 import BeautifulSoup
# import random
# import time
# from fake_useragent import UserAgent

# BESTBUY_PRODUCT_URL = "https://www.bestbuy.com/site/pokemon-trading-card-game-mabosstiff-ex-box/6569192.p?skuId=6569192"
# TEST_CHANNEL_WEBHOOK = 'https://discord.com/api/webhooks/1343432380093825024/2fgCbQigBc0NW8vPVLiCOZ1D5RCo8dnCEdXedu4IIiAjkp1fzvi9sm8eZfSKdlXETbNk'

# ua = UserAgent()

# def get_random_headers():
#     return {
#         "User-Agent": ua.random
#     }


# def check_stock():
#     headers = get_random_headers()
#     print("Current Header: ", headers)
#     print("Checking stock...")

#     response = requests.get(BESTBUY_PRODUCT_URL, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # addtocart_button = soup.find('button', {'class': 'c-button c-button-primary c-button-lg c-button-block c-button-icon c-button-icon-leading add-to-cart-button '})
#     addtocart_button = soup.find('button', {'data-button-state': 'ADD_TO_CART'})

#     if addtocart_button:
#         print("product is in stock!")
#         return True
#     else:
#         print("product is out of stock")
#         return False
    
# if __name__ == "__main__":
#     while True:
#         check_stock()
#         time.sleep(10)

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# options = Options()
# options.add_argument("--headless")  # Run Chrome in headless mode (no UI)
# options.add_argument("--disable-gpu")
# options.add_argument("--window-size=1920,1080")

# BESTBUY_PRODUCT_URL = "https://www.bestbuy.com/site/pokemon-trading-card-game-mabosstiff-ex-box/6569192.p?skuId=6569192"

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# def check_stock():
#     driver.get(BESTBUY_PRODUCT_URL)
#     time.sleep(3)  # Wait for JavaScript to load

#     try:
#         add_to_cart_button = driver.find_element("xpath", "//button[contains(text(), 'Add to Cart')]")
#         if add_to_cart_button.is_displayed():
#             print("🚨 Product is in stock!")
#             return True
#     except:
#         print("Out of stock...")

#     return False

# if __name__ == "__main__":
#     while True:
#         check_stock()
#         time.sleep(60)  # Check every 60 seconds
