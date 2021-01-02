from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from data import *
import time
import requests
from bs4 import BeautifulSoup

import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(base_url)
driver.refresh()
WebDriverWait(driver, 20)
menu = driver.find_elements_by_class_name('cat-n2')

categories = {}

for category in menu:
    category_name = category.find_element_by_tag_name(
        'h2').get_attribute('innerText')
    subcategories = {}
    for subcategory in category.find_elements_by_class_name('cat-n2-list-item'):
        try:
            print(subcategory.find_element_by_tag_name(
                'a').get_attribute('text'))
            subcategories[subcategory.find_element_by_tag_name('a').get_attribute(
                'text')] = subcategory.find_element_by_tag_name('a').get_attribute('href')
        except:
            pass

    categories[category_name] = subcategories

driver.close()
#print(categories)
