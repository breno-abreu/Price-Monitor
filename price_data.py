
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Tuple, Union
import psycopg2
from dotenv import load_dotenv
import os
from psycopg2.extras import DictCursor
import datetime


def get_price(link: str, element_name: str, element_type: str) -> str:
    try:
        price = find_price_with_browser(link, element_name, element_type)
        inclusion_date = datetime.date.today().strftime("%Y-%m-%d")     
        return {'price': price, 'date': inclusion_date}

    except Exception as err:
        return err

def find_price_with_browser(link: str, element_name: str, element_type: str) -> Union[int, str]:
    try:
        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        # Navigate to the webpage
        driver.get(link)

        if element_type == 'class':
            price_str = driver.find_element(By.CLASS_NAME, element_name)
        elif element_type == 'css':
            price_str = driver.find_element(By.CSS_SELECTOR, element_name)
        else:
            return False, 'Element type not found'
        
        # Extract the text content (which is the price value)
        price_str = price_str.text

        # R$ 1.234,56 -> 1234.56
        price_str = price_str.replace('.', '').replace('R$', '')

        # Trim string
        price_str = price_str.strip()

        # 1234.56 -> 1234
        price_str = price_str.split(',')[0]

        # Cast to int
        price_value = int(price_str)

        # Close the browser
        driver.quit()
        
        return price_value

    except Exception as err:
        return err