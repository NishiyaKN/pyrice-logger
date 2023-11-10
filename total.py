from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from datetime import datetime
import json
import time

filename = "price_history.json"
try:
    open(filename,"x")
    file = open(filename,'w')
    file.write("[]")
    print("Created price_history file")
except:
    print("price_history file exists")

today = datetime.today().strftime('%Y-%m-%d')
file = open(filename,"r")
content = file.read()
file.close()

if(content.count(today) == 0):
    print("New day, new query")
    options = Options()
    options.add_argument("--headless")

    browser = webdriver.Firefox(options=options)
    browser.get('https://www.terabyteshop.com.br/produto/18613/monte-seu-pc-gamer-plataforma-amd-ryzen-5000-full-custom?spec=Ja1E2c%2BjzZCEdlQaaL7Re2s0a3dlbHNQVTlEVTM4Q043ZVBtd0hXUzJBM1dVMG92MytyMlgvWCs2eFRidzd5YWdKTHA3bFNTVXJUL1JmQmRSNG1Td1VnUFZ0ZHcyMzNtSnFrTWtyUDJQbVpNM0FFdTVIWE11YjE1UFM2N0Q5TGVyaEdzZnY2TWxRZW1PWFNzYXdzWHkzdnR4YzZWRCsvekU1NnZkNVgzakExV2hSVmQ1TkFlWEhzZHl6RlhTVjlaakJiYU1UOVowRnpxRCtiN0c0SXZqSEgvUlI2dmJwOU1qQmFna1FyZTNtaU43UUh4UEpwckhwNGlScGprbGIwZHVQcC8zbDdpVGd5S1lZcnNMOHpPSk43M3BMMUdBaCtkWUVVNk4xWHY3NlJqeTliaU14TWRyMlFiblBnZWVCQ2FNaVk5U09tZXE3SEhMTDlUeHZMdWIyU0J5djdGSVJ6RmhrcTZHd2JOTGkwaDhGSXFzbUxBSTRvanBXdz0%3D')

    print("Accessing the website")
    time.sleep(10)
    total = browser.find_element(By.ID, 'valVista')
    total_text = total.text
    if total_text == "R$ 0,00":
        print("Error, try again later")
        browser.close()
        exit()
    else: 
        print("Price found, writing...")
        total_text = total_text.split(" ")[1].replace(".","").replace(",",".")
        time.sleep(10)
        new_data = {
                "date":today,
                "price":total_text
        }
        file = open(filename)
        file_data = json.load(file)
        file_data.append(new_data)

        new_file_data = open(filename, 'w')
        json.dump(file_data,new_file_data, indent=4, separators=(',',': '))
        file.close()
        new_file_data.close()

        browser.close()
else:
    print("Already updated today\n")
