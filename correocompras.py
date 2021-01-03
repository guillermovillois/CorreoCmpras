from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from data import *
import time
import requests
from bs4 import BeautifulSoup
import json
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
            subcategories[subcategory.find_element_by_tag_name('a').get_attribute(
                'text')] = subcategory.find_element_by_tag_name('a').get_attribute('href')
        except:
            pass

    categories[category_name] = subcategories

categorias = {}
for category in list(categories.keys()):
    productos = {}
    for subcategory in categories[category]:
        driver.get(categories[category][subcategory])
        speed = 15
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script(
                "window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script(
                "return document.body.scrollHeight")

        soup = BeautifulSoup(driver.page_source, "html.parser")

        products = soup.find('div', {'class': 'product-list'})

        subprod = {}

        try:
            for product in products.findAll('ul'):
                try:
                    id = product.find(
                        'div', {'class': 'box-item'})['id'].split('-')[1]
                    name = product.find(
                        'span', {'class': 'product-description'}).text
                    price = product.find(
                        'span', {'class': "best-price"}).text.split('$')[1]
                    url = product.find('a', {'class': "product-link"})['href']
                    subprod[str(id)] = {'name': name,
                                        'price': price, 'url': url}
                except:
                    pass
        except:
            print(subcategory,  ' Error No data')

        productos[subcategory] = subprod
    categorias[category] = productos

with open('products.json', 'w') as fp:
    json.dump(categorias, fp)

driver.close()
