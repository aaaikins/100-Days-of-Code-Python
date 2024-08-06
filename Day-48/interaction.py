from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://secure-retreat-92358.herokuapp.com/")

first_name = driver.find_element(By.XPATH, value='/html/body/form/input[1]')
first_name.send_keys("Aikins")

last_name = driver.find_element(By.XPATH, value='/html/body/form/input[2]')
last_name.send_keys("Acheampong")

email = driver.find_element(By.XPATH, value='/html/body/form/input[3]')
email.send_keys("aaaaikins@gmail.com")

sign_up = driver.find_element(By.XPATH, value='/html/body/form/button').click()
# sign_up.send_keys(Keys.ENTER)

# driver.quit()
