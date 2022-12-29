from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time
import random

load_dotenv('login.env')

email = os.environ['EMAIL']
password = os.environ['PASS']

def human_input(text, element):
    for l in text:
        time.sleep(random.uniform(0, 0.2))
        element.send_keys(l)

def log_in(driver, email=email, password=password):
    """Logs driver into LinkedIn with given credentials"""

    driver.get("https://www.linkedin.com/login")
    timeout = 60
    try:
        element_present = EC.presence_of_element_located((By.TAG_NAME, "body"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    human_input(email, driver.find_element("id", "username"))
    human_input(password, driver.find_element("id", "password"))
    submit = driver.find_element(By.XPATH, "//button[@class='btn__primary--large from__button--floating']")
    submit.click()

    return driver

driver_wait = 10

def sign_in_prompted(driver):
    WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div['
                                                                                   '2]/div/div/section/main/div/div'
                                                                                   '/div[1]/button'))).click()
    WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '//*['
                                                                                   '@id="public_profile_contextual'
                                                                                   '-sign-in_sign-in'
                                                                                   '-modal_session_key"]')))
    driver.find_element_by_xpath('//*[@id="public_profile_contextual-sign-in_sign-in-modal_session_key"]')\
        .send_keys(email)
    driver.find_element_by_xpath('//*[@id="public_profile_contextual-sign-in_sign-in-modal_session_password"]')\
        .send_keys(password)
    driver.find_element_by_xpath('/html/body/div[2]/div/div/section/main/div/form[1]/div[2]/button').click()

    return driver