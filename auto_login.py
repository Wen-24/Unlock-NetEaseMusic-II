# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00ED23A821F8503EAFC56DAC157F8E280A1FCCE3BE3584610CE2ACA84772F26317A116F72DBEAE6BDD1D761D283771F9A68420D86CC68B32127F1B077D6D61AEB7D4F5D1BA867FC43E6D7509625D6F75E3B88203EE4D29AFA7C096D153F41ABB945E895B8A59E7FE8C6F1D0B4E5C4B50ADD651413D90A92B5545D8CAD7A264767DAE769723058835773E00203BE226D97F2513A08B1E2448A9A09396BD1DC118ED3CCAC96D5A55BA84CC0E02091BBA62195A97E7866812FE916589F9A886DC1C98CE97FE9E9E45878FCF9EF8FEE8055A9F7DFAADCB25AFB322B96B3477E72EBDC3D2177F59E2A7D047194A3DCD3BD095DCED166E0E5204821E20EEE564483CB4DF483B4AF7BA170053445D344EA855533F080CFE5AA337982550760F7FBA2C56B86730E6F9C25B404AAF2B8D900E1BE486156452A63548D1192B7A1875FB0660D668B2C249D98AE1CB33DC274F4B75DB5BEB8A95D62F2CE5FDE690D260DF8520902F64FE1B2AFF28C88FA4097F4A49D5C5499BCA604DFFBFB0B3C53A5CDA72E7BB80B0D4243FDF3A42F719325A7715E6F5"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
