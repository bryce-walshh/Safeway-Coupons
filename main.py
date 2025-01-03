from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time

import json
from llamaapi import LlamaAPI

# Have user to choose their preferences 
import easygui
couponPref = easygui.enterbox("What deals are you looking for? (Meat, Tootpaste, etc.):")


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

# -- LOGGING IN --

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

# -- Clicking Coupons --
time.sleep(15)

more_to_load = True

while(more_to_load):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Load more']")))
        driver.find_element(By.XPATH, "//button[text()='Load more']").click()
        time.sleep(5)

    finally:
        print("Finished!")
        more_to_load = False
    

# Keep clipping Coupons

clip_coupon_buttons = driver.find_elements(By.XPATH, "//button[text()=' Clip Coupon ']")

couponsDetails = driver.find_elements(By.XPATH, "//div[contains(@class, 'cpn-details')]")

coupon_details_arr = []

finished = False

while not finished:

    for coupon in clip_coupon_buttons:
        driver.execute_script("arguments[0].click();", coupon)
        time.sleep(1)
    
    for desc in couponsDetails:
        coupon_details_arr.append(desc.text)

    # Check to see if more coupons have loaded onto the page

    # COMMENTED OUT FOR TESTING
    try:
        clip_coupon_buttons = driver.find_elements(By.XPATH, "//button[text()=' Clip Coupon ']")
        couponsDetails = driver.find_elements(By.CLASS_NAME, "cpn-details")

    except:
        finished = True

    finished = True

print(coupon_details_arr)

time.sleep(5)

driver.quit()
