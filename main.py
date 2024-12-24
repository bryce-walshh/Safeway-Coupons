from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.safeway.com/foru/coupons-deals.html")

# inputting into login

login = driver.find_element(By.ID, 'enterUsername')

phone_num = input("Phone Number: ")
password = input("Password: ")

login.send_keys(phone_num)
login.send_keys(Keys.RETURN)

time.sleep(5)

driver.quit()
