from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver(headless=True):
    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    chrome_options.set_capability(
        "goog:loggingPrefs", {"performance": "ALL"}
    )

    driver = webdriver.Chrome(options=chrome_options)
    return driver
