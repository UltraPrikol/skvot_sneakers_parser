from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from bs4 import BeautifulSoup


option = Options()
option.add_argument("--disable-infobars")
c_service = webdriver.ChromeService(executable_path="F:\ChromeDriver\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=c_service)
wait = WebDriverWait(driver, 10)
URL = "https://www.skvot.com"
driver.get(URL)

close = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "close-modal-btn")))
close.click()

open_search = driver.find_element(By.CLASS_NAME, "search-btn")
open_search.click()

search = driver.find_element(By.NAME, "text")
search.send_keys('Кеды', Keys.RETURN)

time.sleep(1)

items_url = []
items_title = []
items_price = []

soup = BeautifulSoup(driver.page_source, 'lxml')

items = soup.find_all("a", class_='top-item top-item--min')
titles = soup.find_all("div", class_="top-item__title")
prices = soup.find_all("div", class_="top-item__price")

for item in items:
    item_url = URL + item.get("href")
    items_url.append(item_url)

for title in titles:
    item_title = title.text
    items_title.append(item_title)

for price in prices:
    item_price = price.get("data-price")
    items_price.append(item_price)

items_info = {'Название': items_title, 'Цена': items_price, 'Ссылка': items_url}

df = pd.DataFrame(items_info)
print(df)

df.to_excel("skvot_sneakers_info.xlsx")
info = pd.read_excel("skvot_sneakers_info.xlsx")
