from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

load_dotenv('./../login.env')

email = os.environ['EMAIL']
password = os.environ['PASS']
driver_wait = 10
info = []

def scrape(links, driver):
    for profile_link in links:
        driver.get(profile_link)

        WebDriverWait(driver, driver_wait).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div['
                                                  '3]/div/div/div['
                                                  '2]/div/div/main/section['
                                                  '3]/div['
                                                  '3]/div/div/div/span[1]')))

        bio = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[3]/div['
                                           '3]/div/div/div/span[1]').text
        print(bio)
        input()


def login_through_front_page(driver):
    driver.get('https://www.linkedin.com/login')
    WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))) \
        .click()
    driver.find_element_by_id('username').send_keys(email)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/form/div[3]/button').click()


def sign_in_prompted(driver):
    WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div['
                                                                                   '1]/main/div/form/p/button'))) \
        .click()
    WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="session_key"]')))
    driver.find_element_by_xpath('//*[@id="session_key"]').send_keys(email)
    driver.find_element_by_xpath('//*[@id="session_password"]').send_keys(password)
    driver.find_element_by_xpath('/html/body/div[1]/main/div/div/div/form/button').click()

    return driver


if __name__ == '__main__':
    links = ['https://www.linkedin.com/in/olivertoh/']
    driver = webdriver.Chrome()
    # login(driver)
    driver.get(links[0])
    driver = sign_in_prompted(driver)
    scrape(links, driver)
