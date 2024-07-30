import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
zillow_html = response.text
soup = BeautifulSoup(zillow_html, "html.parser")


# Create a list of links for all the listings
listing_a_tags = soup.select('.StyledPropertyCardDataWrapper a')
all_links = [link.get('href') for link in listing_a_tags]
# print(all_links)


# Create a list of prices for all the listings
listing_prices = soup.select('.PropertyCardWrapper__StyledPriceLine')
all_prices = [price.text.replace("/mo", "").split("+")[0] for price in listing_prices]
# print(all_prices)


# Create a list of addresses for all the listings
listing_address = soup.select('address')
address_list = [address.text.strip().replace(' |', '') for address in listing_address]
# print(address_list)


# Use Selenium to fill in your form
driver = webdriver.Chrome()

for address, price, link in zip(address_list, all_prices, all_links):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdr32sLmyHfVUQSv-Dc7g2Vhrv6USSXnPEGNvSHVtMirQmpjw/viewform")
    time.sleep(2)

    address_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/'
                                                  'div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/'
                                                'div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/'
                                               'div/div/div[2]/div/div[1]/div/div[1]/input')

    address_field.send_keys(address)
    price_field.send_keys(price)
    link_field.send_keys(link)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_btn.click()
    time.sleep(2)

# Close the browser
driver.quit()
