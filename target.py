#styles_ndsBaseButton__W8Gl7 styles_md__X_r95 styles_mdGap__9J0yq styles_fullWidth__3XX6f styles_ndsButtonPrimary__tqtKH
#disabled id = addToCartButtonOrTextIdFor88897904
#id = addToCartButtonOrTextIdFor91351689

#link: https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab

import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent

TARGET_PRODUCT_URL = "https://www.target.com/p/pokemon-scarlet-violet-s3-5-booster-bundle-box/-/A-88897904#lnk=sametab"
TARGET_PRODUCT_URL_TEST_STOCK = "https://www.target.com/p/pok-233-mon-trading-card-game-zapdos-ex-deluxe-battle-deck/-/A-91351689#lnk=sametab"
TEST_CHANNEL_WEBHOOK = 'https://discord.com/api/webhooks/1343432380093825024/2fgCbQigBc0NW8vPVLiCOZ1D5RCo8dnCEdXedu4IIiAjkp1fzvi9sm8eZfSKdlXETbNk'

ua = UserAgent()

def get_random_headers():
    return {
        "User-Agent": ua.random
    }


def check_stock():
    headers = get_random_headers()
    print("Current Header: ", headers)
    print("Checking stock...")

    response = requests.get(TARGET_PRODUCT_URL_TEST_STOCK, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open("target_page.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    # addtocart_button = soup.find('button', {'class': 'c-button c-button-primary c-button-lg c-button-block c-button-icon c-button-icon-leading add-to-cart-button '})
    addtocart_button = soup.find('button', {
        'class': 'styles_ndsBaseButton__W8Gl7 styles_md__X_r95 styles_mdGap__9J0yq styles_fullWidth__3XX6f styles_ndsButtonPrimary__tqtKH'})

    if addtocart_button:
        print("product is in stock!")
        return True
    else:
        print("product is out of stock")
        return False
    
if __name__ == "__main__":
    while True:
        check_stock()
        time.sleep(30)