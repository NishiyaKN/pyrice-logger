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
    browser.get('https://www.terabyteshop.com.br/produto/18613/monte-seu-pc-gamer-plataforma-amd-ryzen-5000-full-custom?spec=oUfR6nF761ggqRU9hu%2B6Fm1uRWxXUGhuMURuUXhYNThVcHRBV3JuZHljRlorTSswN3p1UUpGeVFPdHlKWG9qcHkzZkw3bGJhY2pCSEc0ZzlSaTgySE44YXZQQ21mVmU5cnBVaXZ0dXJDNWNCSHFSWXhjczUxdjlJTjJ1dHZ6ZzJYbDNQWUxaZ0dYcFRSUHJENEVUbnNrRTA2aFRRcWJvM3Z5eTNaS1lpQTBZVTVVVzBLb1F5dWVVMnlaNTdRcG1kYkdqTjRqdGx6RysrZUNrd2MzT3l4TTMyZEE4YStONjJoU3M2d25PcS8zMmtxZTJUai9lRmxiOHZqM0tVV0VlemcyZWF3ZEswcjVwUjBkMFBlZkljcmNOT1VSQnVTY0RrN0V2YkQ0NTJvYjJsU2ZGOUptZzgwQTZNbUl4QkhZVTFoWU9TZGFHVU1JbGhqNDFQT1YwNUdnOTZuOHlxZnFOSGM0WW4vZDdzUFhpWlN3VEhHeXRpWTZKRzNSMlpnRk5UcjgrbXJ4UG1xbUdOMXE2d3MyOFd2bVZUbXhaNHNqS000c2lRdmc9PQ%3D%3D')

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
