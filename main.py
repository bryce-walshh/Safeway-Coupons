from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
from groq import Groq
import gui
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
import sys

# -- USER DEAL CUSTOMIZATION --
app = QApplication(sys.argv)
popup = gui.InputPopup()
preferences = ''

# Handling the user input
if popup.exec():  
    if popup.get_input() == '':
        preferences = "No preferences, I just want the best overall deals."
    else:
        preferences = popup.get_input()
else:
    preferences = "No preferences, I just want the best overall deals."

# TODO: Add prompt for login info if it does not already exist 

# -- READ IN USER DATA --
with open("logininfo.txt", "r") as file:
    lines = file.readlines()
    phone_num = lines[0].strip() 
    password = lines[1].strip()
    api_key = lines[2].strip()

options = webdriver.ChromeOptions() 
#options.add_argument("start-minimized")
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
    done = True # random thing for finally syntax


password_inp = driver.find_element(By.ID, 'password')
password_inp.send_keys(password)

#password_inp.send_key(Keys.RETURN)

sign_in_button = driver.find_element(By.XPATH, "//button[text()=' Sign In ']")
sign_in_button.click()

# -- Clicking Coupons --
time.sleep(5)

# Logic to close popups
driver.find_element(By.CLASS_NAME, "onetrust-close-btn-handler").click()
try:
    driver.find_element(By.ID, 'onboardingCloseButton').click()
except:
    print("No onboarding btn, cnt.")


time.sleep(1)

driver.find_element(By.XPATH, "//button[text()='Load more']").click()
    
# Keep clipping Coupons

clip_coupon_buttons = driver.find_elements(By.XPATH, "//button[text()=' Clip Coupon ']")

# TODO: Add additional information on each of the coupons
couponsDetails = driver.find_elements(By.XPATH, "//div[contains(@class, 'cpn-details')]")

coupon_details_arr = []

finished = False

while not finished:

    # for coupon in clip_coupon_buttons:
    #     driver.execute_script("arguments[0].click();", coupon)
    #     time.sleep(1)
    
    for desc in couponsDetails:
        coupon_details_arr.append(desc.text)

    # Check to see if more coupons have loaded onto the page

    # COMMENTED OUT FOR TESTING
    # try:
    #     clip_coupon_buttons = driver.find_elements(By.XPATH, "//button[text()=' Clip Coupon ']")
    #     couponsDetails = driver.find_elements(By.CLASS_NAME, "cpn-details")

    # except:
    #     finished = True

    finished = True

coupon_details_arr = str(coupon_details_arr)

#print(coupon_details_arr)

# LLM API Call to summarize best deals
client = Groq(api_key=api_key)
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": f"Please give me the top 5 deals in these cateogries {preferences} from this list of these coupons: {coupon_details_arr}. Summarize the deals, and do not include any extraneous output such as an introduction."
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(completion.choices[0].message.content + '\n')

time.sleep(5)

# TODO: Add some sort of saving of coupons until they expire

driver.quit()
app.quit()
sys.exit()

