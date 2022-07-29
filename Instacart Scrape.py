import pandas as pd
from bs4 import BeautifulSoup
import regex as re
import numpy as np
import requests
from tqdm import tqdm
import json
from datetime import date
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import DesiredCapabilities

pause_time = 2


# Function to check if log is a json response
def log_filter(log_):
    return (
        # is an actual response
        log_["method"] == "Network.responseReceived"
        # and json
        and "json" in log_["params"]["response"]["mimeType"]
    )


# Make Chrome log requests
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

# Set up driver
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options,
    desired_capabilities=capabilities,
)

# Go to Kroger storefront
driver.get("https://www.instacart.com/store/kroger/storefront")

# Click confirm on location pop-up
driver.find_element(By.CLASS_NAME, "css-4st3dt-content").click()

# Get all menu tabs
tabs = driver.find_elements(By.XPATH, "//a[@class='css-1uowhjo-MenuLink']")

# Set up dictionary of link:text
links = [tab.get_attribute("href") for tab in tabs]
link_text = [tab.text for tab in tabs]

# Irrelevant links - VARIABLE
irrelevant_links = [
    "https://www.instacart.com/store/kroger/collections/2817-ready-meals",
    "https://www.instacart.com/store/kroger/your-lists?source_type=account",
    "https://www.instacart.com/store/kroger/collections/987-deals_tab",
    "https://www.instacart.com/store/kroger/recipes",
    "https://www.instacart.com/store/kroger/collections/dynamic_collection-sales",
    "https://www.instacart.com/store/",
    "https://www.instacart.com/store/account",
    "https://www.instacart.com/store/subscriptions/account?source_type=header_menu_item",
    "https://www.instacart.com/gift-cards",
    "https://www.instacart.com/help",
    "https://www.instacart.com/help/section/how-instacart-works",
    "https://itunes.apple.com/us/app/instacart/id545599256",
    "https://play.google.com/store/apps/details?id=com.instacart.client",
]

# Loop through links
for i, link in enumerate(links):

    # Skip irrelevant links
    if link in irrelevant_links:
        continue

    # Follow link & make soup, then wait
    driver.get(link)
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    time.sleep(pause_time)

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll, wait, check, repeat
    # count = 0
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(pause_time // 1)

        # Calculate new scroll height and compare to last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        # count += 1
        # if count == 3:
        #     break

    # extract item set requests from logs
    item_set_urls = []
    price_set_urls = []
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    for log in filter(log_filter, logs):
        resp_url = log["params"]["response"]["url"]
        if "operationName=Items&" in resp_url:
            item_set_urls.append(resp_url)
        elif "operationName=ItemPricesQuery&" in resp_url:
            price_set_urls.append(resp_url)
    print(len(item_set_urls), len(price_set_urls))

    # Extract data from urls
    item_ids = []
    price_ids = []
    master_items = []
    master_prices = []
    for item_url in item_set_urls:
        try:
            item_data = requests.get(item_url).json()
            for item in item_data["data"]["items"]:
                if item["id"] in item_ids:
                    continue
                master_items.append(
                    [
                        item["id"],
                        item["name"],
                        item["legacyId"],
                        item["legacyV3Id"],
                        item["productId"],
                        item["size"],
                        item["availability"]["available"],
                        item["availability"]["stockLevel"],
                        item["dietary"]["viewSection"]["attributesString"],
                        item["tags"],
                    ]
                )
                item_ids.append(item["id"])
        except Exception as e:
            print("Item Error:", e, item_url)

    for price_url in price_set_urls:
        try:
            price_data = requests.get(price_url).json()
            for price in price_data["data"]["itemPrices"]:
                if price["id"] in price_ids:
                    continue
                master_prices.append(
                    [
                        price["id"],
                        price["itemId"],
                        price["viewSection"]["itemCard"]["priceString"],
                        price["viewSection"]["itemCard"]["pricePerUnitString"],
                        price["viewSection"]["itemCard"]["pricingUnitString"],
                        price["viewSection"]["itemCard"]["pricingUnitSecondaryString"],
                    ]
                )
                price_ids.append(price["id"])
        except Exception as e:
            print("Price Error:", e, price_url)

    # Export dictionaries into csv
    item_frame = pd.DataFrame(
        data=master_items,
        columns=[
            "ID",
            "Name",
            "Legacy ID",
            "Legacy V3 ID",
            "Product ID",
            "Size",
            "Available",
            "Stock Level",
            "Dietary Attributes",
            "Tags",
        ],
    )
    price_frame = pd.DataFrame(
        data=master_prices,
        columns=[
            "ID",
            "Item ID",
            "Price String",
            "Price Per Unit String",
            "Pricing Unit String",
            "Pricing Unit Secondary String",
        ],
    )

    writer = pd.ExcelWriter(
        link_text[i] + "_" + str(date.today())[2:].replace("-", "") + ".xlsx"
    )
    item_frame.to_excel(writer, sheet_name="Items", index=False)
    price_frame.to_excel(writer, sheet_name="Prices", index=False)
    writer.save()
    # break  # REMOVE
