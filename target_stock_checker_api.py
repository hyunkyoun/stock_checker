import requests
import uuid

def generate_visitor_id():
    return uuid.uuid4().hex.upper()

def is_in_stock(tcin: str, location_id: str = "1263", scheduled_store_id: str = "3329"):
    url = "https://redsky.target.com/redsky_aggregations/v1/web/product_fulfillment_and_variation_hierarchy_v1"
    params = {
        "key": "9f36aeafbe60771e321a7cc95a78140772ab3e96",
        "latitude": "40.862661",
        "longitude": "-73.967577",
        "scheduled_delivery_store_id": scheduled_store_id,
        "state": "NJ",
        "zip": "07024",
        "store_id": location_id,
        "paid_membership": "false",
        "base_membership": "true",
        "card_membership": "false",
        "is_bot": "false",
        "tcin": tcin,
        "visitor_id": generate_visitor_id(),
        "channel": "WEB",
        "page": "/p/A-" + tcin
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    fulfillment = data["data"]["product"]["fulfillment"]
    
    shipping_status = fulfillment["shipping_options"]["availability_status"]
    pickup_status = fulfillment["store_options"][0]["order_pickup"]["availability_status"]
    scheduled_status = fulfillment["scheduled_delivery"]["availability_status"]

    return {
        "shipping": shipping_status,
        "pickup": pickup_status,
        "scheduled_delivery": scheduled_status
    }

# Example usage
print(is_in_stock("92327434"))
print(is_in_stock("93954446"))
print(is_in_stock("92538450"))

