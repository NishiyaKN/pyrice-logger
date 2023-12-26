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
USER='inaba'

FILENAME = "/home/" + USER + "/pyrice-logger/vaio/vaio1history.csv"
AUTH_FILE = '/home/' + USER + '/.config/tk/dc'
PRODUCT = 'VAIO FE 15 Ryzen 7 5700U 8gb 256gb'
#LOG = '/home/toki/pyrice-logger/asus/log.txt'

def get_price():
    try: 
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
        browser.get('https://www.br.vaio.com/notebook-vaio-fe15-ryzen-7-8gb-256gb-ssd-prata-titanio-3344016/p')
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        price_element = soup.find('div', {'class': 'vaiobr-loja-1-x-wrapper__preco_por_produto'})  
        price = price_element.text.split('\xa0')[1].replace(".","").replace(",",".").split()[0]
        return price
    except Exception as e:
        print("Something went wrong when getting the price: ", e)
        exit()
    finally:
        browser.close()

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
