import time

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
        time.sleep(2)
        # WebDriverWait(driver, driver_wait).until(
        #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section['
        #                                           '3]/div[3]/div/div/div/span[1]')))

        bio = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[3]/div['
                                           '3]/div/div/div/span[1]').text
        # print(bio)

        container_element = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div['
                                                         '2]/div/div/main/section[5]/div[3]/ul')
        main_ul = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[5]/div['
                                               '3]/ul')
        li_experiences = main_ul.find_elements(By.XPATH, "./child::li")

        for li_elem in li_experiences:
            spans = li_elem.find_elements(By.CSS_SELECTOR, "span[aria-hidden='true']")

            description_and_skills_ul = li_elem.find_element(By.TAG_NAME, "ul")
            description_and_skills_li = description_and_skills_ul.find_elements(By.XPATH, "./child::li")

            print(len(description_and_skills_li))
            description = None

            #check if multiple jobs at same company
            if len(description_and_skills_li) <= 1 or (description_and_skills_li[1].text.find("Skills:") != 0):
                description = description_and_skills_li[0].text
                print(description)
            else:
                # description = description_and_skills_li[0].text
                # print(description)
                pass

            # print(description_and_skills_ul.get_attribute('innerHTML'))
            for li in description_and_skills_li:
                # print(li.text)
                pass
            input()

            description = None

            # for span in spans:
            #     print(span.text)
            # input()


def login_through_front_page(driver):
    driver.get('https://www.linkedin.com/login')
    WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))) \
        .click()
    driver.find_element_by_id('username').send_keys(email)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div[1]/form/div[3]/button').click()


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


if __name__ == '__main__':
    links = ['https://www.linkedin.com/in/olivertoh/']
    driver = webdriver.Chrome()
    login_through_front_page(driver)
    # driver.get(links[0])
    # driver = sign_in_prompted(driver)
    scrape(links, driver)
