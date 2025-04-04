# import asyncio
# from playwright.async_api import async_playwright

# async def run():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         context = await browser.new_context()
#         page = await context.new_page()

#         # Log file to save captured info
#         log_file = open("network_api_capture_verbose.txt", "w", encoding="utf-8")

#         # 🟡 Updated request logger — captures headers + payload
#         def log_request(req):
#             try:
#                 if req.resource_type in ['xhr', 'fetch']:
#                     entry = (
#                         f"\n➡️ {req.method} {req.url}\n"
#                         f"Headers: {req.headers}\n"
#                         f"Post Data: {req.post_data()}\n"
#                         f"{'-'*80}\n"
#                     )
#                     print(entry)
#                     log_file.write(entry)
#             except Exception as e:
#                 log_file.write(f"Error logging request: {e}\n")

#         page.on("request", log_request)

#         # Optional response logger (you can keep it or remove if noisy)
#         async def log_response(response):
#             try:
#                 if response.request.resource_type in ['xhr', 'fetch']:
#                     body = await response.text()
#                     log_file.write(f"⬅️ {response.status} {response.url}\n{body[:1000]}\n{'-'*80}\n")
#             except Exception as e:
#                 log_file.write(f"Error logging response: {e}\n")

#         page.on("response", lambda res: asyncio.create_task(log_response(res)))

#         # Navigate to product page and click "Add to Cart"
#         await page.goto("https://www.target.com/p/lego-speed-champions-mercedes-amg-f1-w15-race-car-building-toy-77244/-/A-92538483")
#         # await page.wait_for_selector('#addToCartButtonOrTextIdFor92538483')
#         # await page.click('#addToCartButtonOrTextIdFor92538483')

#         # Let it run a few seconds to capture network
#         await page.wait_for_timeout(20000)

#         await browser.close()
#         log_file.close()

# asyncio.run(run())
from playwright.async_api import async_playwright
import asyncio

async def sniff_checkout_token():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        token_found = None

        def handle_request(request):
            auth_header = request.headers.get("authorization")
            if auth_header and "Bearer" in auth_header:
                print(f"🔐 Found token in request to {request.url}")
                print(f"Token: {auth_header[:80]}...")  # Print partial token
                nonlocal token_found
                token_found = auth_header.split(" ")[1]

        page.on("request", handle_request)

        # 🔥 Go through the checkout flow manually
        await page.goto("https://www.target.com/co-cart")
        print("👉 Manually proceed through checkout (login, address, etc)...")

        # Let you go through the flow manually and capture request
        await page.wait_for_timeout(60000)  # wait 60 seconds while you check out manually

        await browser.close()
        return token_found

token = asyncio.run(sniff_checkout_token())
if token:
    print("✅ Got usable token:")
    print(token)
else:
    print("❌ No token found.")
