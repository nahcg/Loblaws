from bs4 import BeautifulSoup 
from selenium import webdriver
import pandas as pd
import time
import csv
import regex as re
import html
import numpy as np
import json
import regex as re

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


browser=webdriver.Chrome()
browser.get("https://www.nofrills.ca/food/fruits-vegetables/c/28000")
time.sleep(6)
load = browser.find_elements(By.XPATH, "//div[@class='load-more-button']/button")
browser.find_element(By.XPATH, "//div[@class='lds__privacy-policy__innerWrapper']/button").click()
while len(load) !=0:
    try:
        browser.find_element(By.XPATH, "//div[@class='load-more-button']/button").click()
        time.sleep(1)
    except NoSuchElementException:
        break
soup = BeautifulSoup(browser.page_source, 'lxml')

name = []

names = browser.find_elements(By.XPATH, "//span[@class='product-name__item product-name__item--name']")
for n in names:
    name.append(n.get_attribute("title"))

deal = []
deal2 = []
deals = browser.find_elements(By.XPATH, "//div[@class='product-tile__details__info__text-badge']")
for d in deals:
    deal.append(d.get_attribute("innerHTML"))

for d in deal:
    if d != "":
        c = re.search('(?:product-tile">)(.*)(?:<\/div>)', d)
        c = c.group(1)
        deal2.append(c)
    else:
        deal2.append("")

saleprice = []
saleprice2 = []
itemlist = browser.find_elements(By.XPATH, "//div[@class='product-prices product-prices--product-tile']/div")
for s in itemlist:
    saleprice.append(s.get_attribute('aria-label'))

for s in saleprice:
    if s != None:
        m = re.search("(?:it was )(.*)", s)
        m = m.group(1)
        saleprice2.append(m)
    elif s == None:
        saleprice2.append(s)
       
currprice = []
price = browser.find_elements(By.XPATH, "//div[@class='selling-price-list__item']/span[@class='price selling-price-list__item__price selling-price-list__item__price--now-price']/span[1]")
for i in price:
    currprice.append(i.get_attribute("innerHTML"))

print(len(name))
print(len(currprice))
print(len(saleprice2))
print(len(deal2))

final = pd.DataFrame(
    {'Name': name,
     'Price': currprice,
     'Sale': saleprice2,
     'Deal': deal2
    })

#df = pd.DataFrame.from_records(clean)
final.to_csv("Nfinal.csv")
