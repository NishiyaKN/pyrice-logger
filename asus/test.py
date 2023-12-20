from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.get('https://www.google.com')
print(driver.page_source)
driver.close()
display.stop()
