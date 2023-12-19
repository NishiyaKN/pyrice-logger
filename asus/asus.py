from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from datetime import datetime
import pandas as pd

filename = "asus.csv"

def get_price():
    try: 
        # Don't open a graphical window
        options = Options()
        options.add_argument("--headless")
        # Make the get request
        browser = webdriver.Firefox(options=options)
        browser.get('https://br.store.asus.com/notebook-asus-vivobook-m1502ia.html')
        # Click the cookie button to accept it all
        btn_cookies = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]')
        btn_cookies.click()
        # Scroll to make the specs button visible
        browser.execute_script("window.scrollTo(0,600)")
        # Click to select the right specs
        button = browser.find_element(By.XPATH, '//*[@id="option-label-configuracoes_notebook-1440-item-17509"]')
        button.click()
        # Wait to get the price 
        wait = WebDriverWait(browser, 2)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/main/div[2]/div/div[1]/div[3]/form/div[2]/div/div[1]/div[1]/span[1]/div/span[1]/span[1]/span')))

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        price_element = soup.find('span', {'class': 'price'})  
        price = price_element.text.split('\xa0')[1].replace(".","").replace(",",".")
        return price
    except:
        print("Something went wrong when getting the price")
    finally:
        browser.close()

def get_date():
    today = datetime.today().strftime('%Y-%m-%d')
    return today

def new_dataframe():
    price_today = get_price()
    date_today = get_date()

    dados = pd.DataFrame({
        'Price':[price_today],
        'Date':[date_today]
        })

    # Concatenate the old dataframe with the new one
    old_dataframe = pd.read_csv(filename, index_col=0)
    dataframe=pd.concat([old_dataframe,dados])

    # Resets index so that the new data don't have index 0
    dataframe.reset_index(drop=True, inplace=True)

    dataframe.to_csv(filename)
    print(dataframe)

new_dataframe()

