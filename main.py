from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open("logininfo.txt", "r") as file:
    lines = file.readlines()
    phone_num = lines[0].strip() 
    password = lines[1].strip()

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.safeway.com/foru/coupons-deals.html")

# inputting into login

login = driver.find_element(By.ID, 'enterUsername')

login.send_keys(phone_num)
login.send_keys(Keys.RETURN)

try:
    password_inp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
finally:
    print(driver.title)
    #driver.quit()


password_inp = driver.find_element(By.ID, 'password')
password_inp.send_keys(password)

time.sleep(5)

password_inp.send_key(Keys.RETURN)


time.sleep(5)

driver.quit()
