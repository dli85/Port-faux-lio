from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from google.cloud import storage
from dotenv import load_dotenv
import os

os.environ.setdefault("GCLOUD_PROJECT", "beautiful-curry")

load_dotenv('../login.env')

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


def log_in(driver, email, password):
    """Logs driver into LinkedIn with given credentials"""

    driver.get("https://www.linkedin.com/login")
    timeout = 60
    try:
        element_present = EC.presence_of_element_located((By.TAG_NAME, "body"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

    driver.find_element("id", "username").send_keys(email)
    driver.find_element("id", "password").send_keys(password)
    submit = driver.find_element(By.XPATH, "//button[@class='btn__primary--large from__button--floating']")
    submit.click()

    return driver


def save_headshot(driver, local_path, profile_link):
    """Saves the headshot of the given link to the given path"""
    driver.get(profile_link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    div = soup.find('div', {"class": "pv-top-card__non-self-photo-wrapper ml0"})
    html_img = soup.find('img', {
        "class": "pv-top-card-profile-picture__image pv-top-card-profile-picture__image--show ember-view"})
    img_src = html_img.attrs['src']

    r = requests.get(img_src, stream=True)
    image = r.content
    print(len(image))
    if r.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(r.content)
    else:
        print("error saving headshot" + local_path)


if __name__ == "__main__":
    links = ["https://www.linkedin.com/in/olivertoh/", "https://www.linkedin.com/in/david-li-0690aa17a"]
    driver = log_in(webdriver.Chrome(), EMAIL, PASS)

    for i, l in enumerate(links):
        local_path = "headshots/images/img_{}.jpg".format(i)
        save_headshot(driver, local_path, l)
        upload_blob(local_path, "indian/igs_{}.jpg".format(i))

    driver.quit()
