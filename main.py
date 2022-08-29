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

def main(BASE_URL: str = BASE_URL, RESTAURANT_LIST_SUFFIX: str = RESTAURANT_LIST_SUFFIX, search_string: str = 'poznan-poznan-grunwald-61-801?sortBy=name'):
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=set_chrome_options())
    driver.get('https://www.pyszne.pl/na-dowoz/jedzenie/poznan-poznan-grunwald-61-801?sortBy=name')
    restaurant_count = WebDriverWait(driver, timeout=3).until(EC.presence_of_element_located((By.XPATH, "//*[@id='page']/div[4]/section/div[1]/div/div[2]/div/h1")))
    restaurant_count = int(re.findall('[0-9]+', restaurant_count.text)[0])

    restaurant_list = []
    restaurant_list_count_history = []

    def _get_restaurants():
        restaurant_list = restaurant_list.append(WebDriverWait(driver, timeout=3).until(lambda x: x.find_elements(By.TAG_NAME, "li")))
        restaurant_list_count_history.append(len(restaurant_list))

        # check if the amount of restaurants loaded is less than top of the page says
        # if there aren't any more retaurants to be loaded, stop
        if (len(restaurant_list) < restaurant_count) & (len(restaurant_list_count_history) == len(set(restaurant_list_count_history))):
            ActionChains(driver).scroll_to_element(restaurant_list[-1]).perform()
            _get_restaurants()
        else:
            pass
        return None

    _get_restaurants()

    return restaurant_list

if __name__ == '__main__':
    print(main())