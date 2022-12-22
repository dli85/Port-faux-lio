from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from google.cloud import storage
from dotenv import load_dotenv
import os
import concurrent.futures
from dataset import log_in, upload_blob
import pandas as pd
#from ethnicolr import pred_wiki_name

os.environ.setdefault("GCLOUD_PROJECT", "beautiful-curry")

load_dotenv('../login.env')

# set your env variable EMAIL and PASS
EMAIL = os.environ['EMAIL']
PASS = os.environ['PASS']

BUCKET_NAME = "linkedin-headshots"

def collect_profiles(query, driver, out_csv):
    print(query)
    df = pd.DataFrame(columns=["fullname", "headline", "url", "headshot_src"])

    for i in range(1, 2):
        print(i)
        keywords = query.replace(" ", "%20")
        url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=SWITCH_SEARCH_VERTICAL&page={}".format(keywords, i)
        driver.get(url)

        profile_list = driver.find_elements(By.CLASS_NAME, "entity-result__item")
        page_profiles = {"fullname":[], "headline":[], "url":[], "headshot_src":[]}

        for profile in profile_list:
            print(profile.page_source)
            url = profile.find_element(By.XPATH,\
             "//span[@class='entity-result__title-textt-16']/a[@class='app-aware-link']").get_attribute('href')

            fullname = profile.find_element(By.XPATH,\
             "//span[@class='entity-result__title-textt-16']/a[@class='app-aware-link']/\
                span/span[@class='visually-hidden']").text

            try:
                headline = profile.find_element(By.XPATH,\
                "//div[@class='linked-area flex-1 cursor-text']/a[@class='app-aware-link']/\
                    div[@class='entity-result__primary-subtitle t-14 t-black t-normal']").text
            except:
                headline = ""

            try:
                img_src = driver.find_element(By.XPATH,\
                    "//img[@class='presence-entity__image\  ivm-view-attr__img--centered EntityPhoto-circle-3\
                        EntityPhoto-circle-3 lazy-image ember-view']").get_attribute("src")
            except:
                img_src = ""

            page_profiles["fullname"].append(fullname)
            page_profiles["headline"].append(headline)
            page_profiles["url"].append(url)
            page_profiles["headshot_src"].append(img_src)
        
        page_df = pd.DataFrame(page_profiles)
        """odf = pred_wiki_name(page_df,'fullname', conf_int=0.9)
        filtered_df = page_df[odf["race"]=="Asian,IndianSubContinent"]
        pd.concat([df, filtered_df])"""
        pd.concat([df, page_df])

    df.to_csv(out_csv, mode='a', index=False, header=False)


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = log_in(webdriver.Chrome(options=options), EMAIL, PASS)

    studies = ['computer science', 'data science', 'electrical engineering', 'mechanical engineering']
    studies = ['computer science']

    for s in studies:
        search_query = "ms {} northeastern".format(s)
        collect_profiles(search_query, driver, "profile_list.csv")
    
    upload_blob("profile_list.csv", "profile_list.csv")
    
    driver.quit()
