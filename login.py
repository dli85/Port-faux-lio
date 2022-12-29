from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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