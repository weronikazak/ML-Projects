from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)/chromedriver.exe"

driver = webdriver.Chrome(PATH)
driver.maximize_window()

driver.get("https://www.youtube.com/")

search = driver.find_element_by_name("search_query")
search.send_keys("GŁOWA W BETONIARCE")
search.send_keys(Keys.RETURN)

currentUrl = driver.current_url
driver.get(currentUrl)

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "video-title"))
    )
finally:
    driver.find_elements_by_id('video-title')[1].click()
    time.sleep(1)
    driver.find_element_by_class_name("ytp-fullscreen-button").click()
    time.sleep(400)




















search = driver.find_element_by_name("search_query")
search.send_keys("GŁOWA W BETONIARCE")
search.send_keys(Keys.RETURN)

currentUrl = driver.current_url
driver.get(currentUrl)

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "video-title"))
    )
finally:
    driver.find_element_by_id('video-title').click()


