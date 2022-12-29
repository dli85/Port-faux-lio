from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from google.cloud import storage
from dotenv import load_dotenv
import os
from PIL import Image
from login import log_in
import concurrent.futures
import time
import random

os.environ.setdefault("GCLOUD_PROJECT", "beautiful-curry")

load_dotenv('./../login.env')

# set your env variable EMAIL and PASS
EMAIL = os.environ['EMAIL']
PASS = os.environ['PASS']

BUCKET_NAME = "linkedin-headshots"


def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket and deletes the local file."""
    # The ID of your GCS bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    # print(
    # f"File {source_file_name} uploaded to {destination_blob_name}."
    # )

    os.remove(source_file_name)


def human_input(text, element):
    for l in text:
        time.sleep(random.uniform(0, 0.2))
        element.send_keys(l)


def save_headshot(driver, local_path, profile_link):
    """Saves the headshot of the given link to the given path"""
    driver.get(profile_link)
    html = driver.page_source
    #print(html)
    img_src = driver.find_element(By.XPATH, "//img[@class='pv-top-card-profile-picture__image pv-top-card-profile-picture__image--show ember-view']").get_attribute("src")

    r = requests.get(img_src, stream=True)
    if r.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(r.content)
        img = Image.open(local_path)
        #print(img.size)
        if img.size != (400, 400):
            resized = img.resize((400, 400))
            resized.save(local_path)
    else:
        print("error saving headshot" + local_path)


if __name__ == "__main__":
    links = ["https://www.linkedin.com/in/olivertoh/", "https://www.linkedin.com/in/david-li-0690aa17a"]
    
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = log_in(webdriver.Chrome(options=options), EMAIL, PASS)

    for i, l in enumerate(links):
        local_path = "images/img_{}.jpg".format(i)
        save_headshot(driver, local_path, l)
        upload_blob(local_path, "indian/igs_{}.jpg".format(i))

    driver.quit()
