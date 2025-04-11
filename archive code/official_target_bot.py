import asyncio
import requests
from playwright.async_api import async_playwright
import random

EMAIL = ""
PASSWORD = ""
CVV = ""
TCIN = "89444928"
QUANTITY = 1

def add_to_cart(session, headers, tcin, quantity):
    url = "https://carts.target.com/web_checkouts/v1/cart_items?field_groups=CART,CART_ITEMS,SUMMARY&key=9f36aeafbe60771e321a7cc95a78140772ab3e96"
    payload = {
        "cart_item": {
            "item_channel_id": "10",
            "tcin": tcin, 
            "quantity": quantity
        },
        "cart_type": "REGULAR",
        "channel_id": "10",
        "shopping_context": "DIGITAL"
    }

    response = session.post(url, headers=headers, json=payload)
    data = response.json()

    print("✅ Item added to cart.")
    cart_id = data.get("cart_id")
    return cart_id

def convert_cookies_to_jar(cookies):
    jar = requests.cookies.RequestsCookieJar()
    access_token = None

    for cookie in cookies:
        jar.set(
            name=cookie['name'],
            value=cookie['value'],
            domain=cookie.get('domain', '.target.com'),
            path=cookie.get('path', '/')
        )
        if cookie['name'] == 'accessToken':
            access_token = cookie['value']

    return jar, access_token

async def open_website(tcin, quantity, email, password, cvv):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to Target's homepage to set initial cookies
        await page.goto("https://www.target.com")

        # 2. Click on the element with data-account-sign-in
        await page.locator('#account-sign-in').click()

        # 3. Click the button with id "accountNav-signIn"
        await page.locator('[data-test="accountNav-signIn"]').click()

        # 4. Fill in the email input
        await page.locator('#username').fill(email)  # Replace with your actual email

        # 5. Click the "Continue" button (id="login")
        await page.locator('#login').click()

        # 6. Fill in the password field
        await page.locator('#password').fill(password)  # Replace with your actual password

        # 7. Click the "Sign in with password" button (also id="login" but with different text)
        await page.locator('#login:has-text("Sign in with password")').click()

        await page.wait_for_timeout(1750)  # Let cookies load

        cookies = await context.cookies()

        jar, access_token = convert_cookies_to_jar(cookies)

        if not access_token:
            print("❌ accessToken not found in cookies. Try reloading the page longer in Playwright.")
            exit()

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "x-api-key": "9f36aeafbe60771e321a7cc95a78140772ab3e96",
            "x-application-name": "web",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }

        session = requests.Session()
        session.cookies.update(jar)

        try:
            cart_id = add_to_cart(session, headers, tcin, quantity)
            # get_cart_contents(session, headers)
        except Exception as e:
            print("❌ Something went wrong:", e)

        await page.goto("https://www.target.com/cart")

        await page.locator('[data-test="checkout-button"]').click()

        await page.locator('[data-test="placeOrderButton"]').click()

        await page.locator('#enter-cvv').fill(cvv)

        for _ in range(5):
            try:
                # Wait for button to appear (or timeout quickly if it's not there)
                await page.wait_for_selector('[data-test="confirm-button"]', timeout=2000)
                # await page.locator('[data-test="confirm-button"]').click()
                await page.wait_for_timeout(random.randint(300, 500))
            except TimeoutError:
                print("❌ Confirm button not found — exiting loop.")
                break

        await page.wait_for_timeout(10000)  # Let the cart load


        await browser.close()
        return cookies

if __name__ == "__main__":
    asyncio.run(open_website("89444928", 1, EMAIL, PASSWORD, CVV))