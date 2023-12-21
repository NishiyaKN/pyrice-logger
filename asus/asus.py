from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from datetime import datetime
import pandas as pd
import requests

#from pyvirtualdisplay import Display
#display = Display(visible=0, size=(800, 600))
#display.start()

FILENAME = "/home/toki/pyrice-logger/asus/asus.csv"
AUTH_FILE = '/home/toki/.config/tk/dc'
PRODUCT = 'Vivobook M1502IA'
LOG = '/home/toki/pyrice-logger/asus/log.txt'

def get_price():
    try: 
        options = Options()
        options.add_argument("--headless")
        print(1)
        browser = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
        browser.get('https://br.store.asus.com/notebook-asus-vivobook-m1502ia.html')
        print(2)
        # Click the cookie button to accept it all
        btn_cookies = browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]')
        btn_cookies.click()
        print(3)
        # Scroll to make the specs button visible
        browser.execute_script("window.scrollTo(0,1000)")
        # Click to select the right specs
        print(3.7)
        button = browser.find_element(By.XPATH, '//*[@id="option-label-configuracoes_notebook-1440-item-17509"]')
        button.click()
        #with open(LOG,'w') as l:
        #    l.write(browser.page_source)
        #print(browser.page_source)
        #print(4)
        # Wait to get the price 
        #wait = WebDriverWait(browser, 120)
        #print(4.8)
        #wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/main/div[2]/div/div[1]/div[3]/form/div[2]/div/div[1]/div[1]/span[1]/div/span[1]/span[1]/span')))

        print(5)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        print(6)
        price_element = soup.find('span', {'class': 'price'})  
        price = price_element.text.split('\xa0')[1].replace(".","").replace(",",".")
        print(7)
        return price
    except Exception as e:
        print("Something went wrong when getting the price: ", e)
        exit()
    #finally:
        #browser.close()

def get_date():
    today = datetime.today().strftime('%Y-%m-%d')
    return today

def check_new_price(old_dataframe, dados):
    last_price = old_dataframe.loc[len(old_dataframe) - 1]['Price']
    new_price = float(dados.loc[0]['Price'])
    if last_price != new_price:
        print("Price is different, sending discord notification...")
        if last_price > new_price:
            comment = 'cheaper'
        else:
            comment = 'more expensive'
        notify_discord(new_price,comment)
    else:
        print("The price is the same as before")

def notify_discord(new_price,comment):
    with open(AUTH_FILE,'r') as f:
        auth = f.read()

    url = 'https://discord.com/api/v9/channels/1180832500403155095/messages' 
    headers = {
            "Authorization" : auth.strip()
    }
    payload = {
            "content": "Price for " + PRODUCT + " is now " + comment + " : " + str(new_price)
    }

    res = requests.post(url, payload, headers=headers)
    print("Discord message sent" + res)

def main():
    old_dataframe = pd.read_csv(FILENAME, index_col=0)
    date_today = get_date()
    latest_day = old_dataframe.loc[len(old_dataframe) - 1]['Date']

    if date_today != latest_day:
        price_today = get_price()
        dados = pd.DataFrame({
            'Price':[price_today],
            'Date':[date_today]
            })

        # Concatenate the old dataframe with the new one
        dataframe=pd.concat([old_dataframe,dados])

        # Resets index so that the new data don't have index 0
        dataframe.reset_index(drop=True, inplace=True)

        dataframe.to_csv(FILENAME)
        check_new_price(old_dataframe,dados)
        print(dataframe)
    else:
        print("Nothing to update for today")

if __name__ == '__main__':
    main()
