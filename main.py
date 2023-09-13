from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

google_form = "https://docs.google.com/forms/d/e/1FAIpQLSc9h-xt6dZCZ5REoPOW80AkqdnwZBNeyZKVCVFUIdtKnS2Bog/viewform?usp=sf_link"
zillow = "https://shorturl.at/cnuG2"
header = {
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

webpage = requests.get(zillow, headers=header)
html = webpage.text
soup = BeautifulSoup(html, "html.parser")

items = soup.find_all(class_="property-card-link")
image_link = [f"https://www.zillow.com{list.get('href')}" if "zillow" not in list else list.get("href") for list in
              items]

price_tag = soup.find_all(name="span", attrs={"data-test": "property-card-price"})
price_list = [price.getText() for price in price_tag]

address_tag = soup.find_all(name="address", attrs={"data-test": "property-card-addr"})
address_list = [address.getText() for address in address_tag]

driver = webdriver.Edge()
driver.get(google_form)

for n in range(0, len(address_list)):
    time.sleep(2)
    address_input = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
        address_list[n])
    price_per_month = driver.find_element(By.XPATH,
                                          '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
        price_list[n])
    property_link = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
        image_link[n])
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()
    another_response = driver.find_element(By.TAG_NAME, "a").click()
