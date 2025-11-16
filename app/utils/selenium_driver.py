from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Add more options later

    return webdriver.Chrome(options=options)
