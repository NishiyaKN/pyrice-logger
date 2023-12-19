from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from datetime import datetime
import json
import time

filename = "individual_price.json"
component_num = 5
price_error = ""

try:
    open(filename,"x")
    file = open(filename,'w')
    file.write('{\n    "RX 6600": [],\n    "RX 6500 XT":[],\n    "5 5600":[],\n    "5 5500":[],\n    "5 4600G":[]\n}')
    file.close()
    print("Created",filename,"file")
except:
    print(filename,"file exists")

options = Options()
options.add_argument("--headless")

def get_price(num):
    browser = webdriver.Firefox(options=options)
    match num:
        case 0:
            component = "RX 6600"
            browser.get('https://www.terabyteshop.com.br/produto/19808/placa-de-video-asrock-radeon-rx-6600-challenger-d-8gb-gddr6-fsr-ray-tracing-90-ga2rzz-00uanf')
        case 1:
            component = "RX 6500 XT"
            browser.get('https://www.terabyteshop.com.br/produto/20245/placa-de-video-powercolor-radeon-rx-6500-xt-4gb-gddr6-fsr-ray-tracing-axrx-6500-xt-4gbd6-dh')
        case 2:
            component = "5 5600"
            browser.get('https://www.terabyteshop.com.br/produto/20788/processador-amd-ryzen-5-5600-35ghz-44ghz-turbo-6-cores-12-threads-cooler-wraith-stealth-am4-100-100000927box')
        case 3:
            component = "5 5500"
            browser.get('https://www.terabyteshop.com.br/produto/20782/processador-amd-ryzen-5-5500-36ghz-42ghz-turbo-6-cores-12-threads-cooler-wraith-stealth-am4-100-100000457box')
        case 4:
            component = "5 4600G"
            browser.get('https://www.terabyteshop.com.br/produto/21317/processador-amd-ryzen-5-4600g-37ghz-42ghz-turbo-6-cores-12-threads-cooler-wraith-stealth-am4-100-100000147box')
        
    print("Accessing the website for",component)
    # time.sleep(10)
    data = browser.find_element(By.ID, 'valVista')
    data = data.text
    if data == "R$ 0,00":
        print("Error retrieving",component," price. Try again later")
        global price_error
        price_error += component
        browser.close()
    elif data == "":
        print("PRODUTO INDISPONIVEL")
    else: 
        print("Price found, writing...")
        # time.sleep(10)
        try:
            # Terabyteshop only
            data = data.split(" ")[1].replace(".","").replace(",",".")
            new_data = {
                    "date":today,
                    "price":data
            }
            print("preco: ", data)
            file = open(filename)
            file_data = json.load(file)
            # if component not in file_data:
            #     file_data[component] = []  # Create an empty list if it doesn't exist
            file_data[component].append(new_data)
            print("file_data:",file_data[component])

            new_file_data = open(filename, 'w')
            json.dump(file_data,new_file_data, indent=4, separators=(',',': '))

            print("Price recorded successfully")
            file.close()
            new_file_data.close()
        except Exception as e:
            print(f"Erro: {e}")
        browser.close()

today = datetime.today().strftime('%Y-%m-%d')
file = open(filename,"r")
content = file.read()
file.close()

if(content.count(today) == 0):
    print("New day, new query")
    for i in range(component_num):
        get_price(i)
    if price_error != "":
        print("PRICES WITH ERROR: ", price_error)
else:
    print("Already done the daily update")
    i = int(input("Manually retrieve price of which component?\n0- RX 6600\n1- RX 6500 XT\n2- 5 5600\n3- 5 5500\n4- 4600G\n"))
    if i >= 0 and i < component_num:
        get_price(i)
        if price_error != "":
            print("PRICES WITH ERROR: ", price_error)
    else:
        print("Invalid option")
