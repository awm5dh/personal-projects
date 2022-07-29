import requests
import json
from datetime import date

url = "https://www.instacart.com/graphql?operationName=Items&variables=%7B%22ids%22%3A%5B%22items_29299-19183699%22%2C%22items_29299-3401790%22%2C%22items_29299-18578704%22%2C%22items_29299-427254%22%2C%22items_29299-19019742%22%2C%22items_29299-17315439%22%2C%22items_29299-3254797%22%2C%22items_29299-3282189%22%2C%22items_29299-43210%22%2C%22items_29299-122841%22%5D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22e8a86ec6c9378c14f909b1c44023b9c9a75299521cf6b646f6eaba0a37a66d84%22%7D%7D"
# response = requests.get(url)
# data = response.json()
# for item in data["data"]["items"]:  # data["data"]["itemPrices"]
#     print(json.dumps(item, indent=4, sort_keys=True))

price_url = "https://www.instacart.com/graphql?operationName=ItemPricesQuery&variables=%7B%22ids%22%3A%5B%22items_29299-16410957%22%2C%22items_29299-16564380%22%2C%22items_29299-41737%22%2C%22items_29299-19916681%22%2C%22items_29299-3253874%22%2C%22items_29299-122841%22%2C%22items_29299-19280264%22%2C%22items_29299-43123%22%2C%22items_29299-3282726%22%2C%22items_29299-41722%22%5D%2C%22shopId%22%3A%225395%22%2C%22zoneId%22%3A%221350%22%2C%22postalCode%22%3A%2238655%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22a4d969474bfdf8506b7744e989e226eb09cb04b59f84c9b586ef368276b1c14b%22%7D%7D"
# price_response = requests.get(price_url)
# price_data = price_response.json()
# for item in price_data["data"]["itemPrices"]:
#     print(json.dumps(item, indent=4, sort_keys=True))

print(str(date.today())[2:].replace("-", ""))
