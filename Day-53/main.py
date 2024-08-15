from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Part 1 - Scrape the links, addresses, and prices of the rental properties

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# Use our Zillow-Clone website (instead of Zillow.com)
response = requests.get("https://appbrewery.github.io/Zillow-Clone/", headers=header)

data = response.text
soup = BeautifulSoup(data, "html.parser")

# Create a list of all the links on the page using a CSS Selector
all_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
all_links = [link["href"] for link in all_link_elements]
print(f"There are {len(all_links)} links to individual listings in total: \n")
print(all_links)

# Create a list of all the addresses on the page using a CSS Selector
all_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
all_addresses = [address.get_text().replace(" | ", " ").strip() for address in all_address_elements]
print(f"\nAfter having been cleaned up, the {len(all_addresses)} addresses now look like this: \n")
print(all_addresses)

# Create a list of all the prices on the page using a CSS Selector
all_price_elements = soup.select(".PropertyCardWrapper span")
all_prices = [price.get_text().replace("/mo", "").split("+")[0].strip() for price in all_price_elements if
              "$" in price.text]
print(f"\nAfter having been cleaned up, the {len(all_prices)} prices now look like this: \n")
print(all_prices)

# Part 2 - Fill in the Google Form using Selenium

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(all_links)):
    try:
        # TODO: Replace with your own Google Form link
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdiOFdbmCkocWnA1JDS82sxaRZmV-xUZWk-I5ReDTins543EQ/viewform?usp=sf_link")

        # Wait until the elements are present on the page before interacting
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
        )

        address = driver.find_element(by=By.XPATH,
                                      value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price = driver.find_element(by=By.XPATH,
                                    value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link = driver.find_element(by=By.XPATH,
                                   value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        submit_button = driver.find_element(by=By.XPATH,
                                            value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

        address.send_keys(all_addresses[n])
        price.send_keys(all_prices[n])
        link.send_keys(all_links[n])
        submit_button.click()

        # Wait for the form to submit
        WebDriverWait(driver, 10).until(
            EC.url_changes(driver.current_url)
        )

    except (TimeoutException, NoSuchElementException) as e:
        print(f"An error occurred: {e}")
        continue

# Optional: Close the browser at the end of the script
# driver.quit()
