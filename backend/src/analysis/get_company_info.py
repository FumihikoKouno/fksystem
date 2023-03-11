from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
import io
import os
import time
import pandas

# 定数定義
GOOGLE_URL='https://google.co.jp'
DRIVER_PATH = './driver/chromedriver.exe'
MAX_PAGE=10
SEARCH_TARGET = 'fujitsu'

# 接続
service = service.Service(executable_path=DRIVER_PATH)
driver = webdriver.Chrome(service=service)
time.sleep(1)

driver.get(GOOGLE_URL)
time.sleep(3)
elements = driver.find_elements(by=By.TAG_NAME, value='input')
for element in elements:
    if element.get_attribute('title') == '検索':
        element.send_keys(SEARCH_TARGET)
        break

time.sleep(1)
elements = driver.find_elements(by=By.TAG_NAME, value='input')

for element in elements:
    if element.get_attribute('value') == 'Google 検索':
        element.click()
        break

time.sleep(3)

search_result = driver.find_element(by=By.ID, value='result-stats')
print(search_result.text.split(' ')[1])




driver.close()
