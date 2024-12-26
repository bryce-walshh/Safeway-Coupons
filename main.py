from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


with open("logininfo.txt", "r") as file:
    lines = file.readlines()
    phone_num = lines[0].strip() 
    password = lines[1].strip()

options = webdriver.ChromeOptions() 
#options.add_argument("start-maximized")
driver = uc.Chrome(options=options)

#driver = webdriver.Chrome(ChromeDriverManager().install())

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

#password_inp.send_key(Keys.RETURN)

sign_in_button = driver.find_element(By.XPATH, "//button[text()=' Sign In ']")
sign_in_button.click()


time.sleep(20)

driver.quit()
