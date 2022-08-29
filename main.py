from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re

BASE_URL = 'https://www.pyszne.pl/'
RESTAURANT_LIST_SUFFIX = 'na-dowoz/'

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def get_page_height(driver: webdriver) -> int:
    '''
    Returns the page height if passed a webdriver.
    '''
    return driver.execute_script('return document.body.scrollHeight')

def main(BASE_URL: str = BASE_URL, RESTAURANT_LIST_SUFFIX: str = RESTAURANT_LIST_SUFFIX, search_string: str = 'poznan-poznan-grunwald-61-801?sortBy=name'):
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=set_chrome_options())
    driver.get('https://www.pyszne.pl/na-dowoz/jedzenie/poznan-poznan-grunwald-61-801?sortBy=name')
    driver.implicitly_wait(15)

    restaurant_list = []
    reached_page_end = False
    last_height = get_page_height(driver=driver)

    while not reached_page_end:
        restaurant_list = WebDriverWait(driver, timeout=10).until(lambda x: x.find_elements(By.TAG_NAME, "li"))
        ActionChains(driver).scroll_to_element(restaurant_list[-1]).perform()
        current_height = get_page_height(driver=driver)

        if last_height == current_height:
            reached_page_end = True
        else:
            last_height = current_height

    return restaurant_list

if __name__ == '__main__':
    print(main())