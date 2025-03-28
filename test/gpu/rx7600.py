# This script creation was heavily assisted by AI using the scripts from asus and pc_hardware directories as a base

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import json
import time
import requests

filename = "rx7600_price.json"
component_num = 12
price_error = ""

# Initialize JSON file
try:
    with open(filename, "x") as file:
        json.dump({
            "P - ASUS": [], "P - XFX": [], "P - ASROCK": [], "P - GIGABYTE": [],
            "T - ASUS": [], "T - XFX": [], "T - ASROCK": [], "T - ASROCK (Steel Legend)": [],
            "K - GIGABYTE": [], "K - XFX": [], "K - ASROCK (Steel Legend)": [], "K - ASROCK": []
        }, file, indent=4)
    print("Created", filename)
except FileExistsError:
    print(filename, "already exists")

def notify_discord(component, new_price, old_price=None):
    """Send price updates to Discord"""
    try:
        with open('/home/yori/.config/tk/dc', 'r') as f:
            token = f.read().strip()
        
        headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }
        
        # Customize your message format
        if old_price:
            change = float(new_price) - float(old_price)
            arrow = "🔽" if change < 0 else "🔼"
            message = (
                f"{arrow} Price change for {component}\n"
                f"Old: R$ {old_price}\n"
                f"New: R$ {new_price}\n"
                f"Change: R$ {abs(change):.2f}"
            )
        else:
            message = f"📊 Initial price for {component}: R$ {new_price}"
            
        requests.post(
            "https://discord.com/api/v9/channels/1180832500403155095/messages",
            json={"content": message},
            headers=headers
        )
        
    except Exception as e:
        print(f"Discord notification failed: {str(e)}")

# Browser setup
options = Options()
# options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")  # Keep disabled for debugging

def close_terabyte_popups(browser):
    """Handles all possible Terabyte popups independently"""
    popups_closed = 0
    
    # Try closing the floating popup (button)
    try:
        # Switch to iframe if exists
        try:
            WebDriverWait(browser, 3).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='modal']"))
            )
            in_frame = True
        except:
            in_frame = False
            
        close_btn = WebDriverWait(browser, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.tsG0HQh7bcmTha7pyanx-btn-close"))
        )
        close_btn.click()
        popups_closed += 1
        print("✅ Closed floating popup")
    except:
        pass
    finally:
        if in_frame:
            browser.switch_to.default_content()

    # Try closing the newsletter popup (span)
    try:
        close_btn = WebDriverWait(browser, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.fa-times"))
        )
        close_btn.click()
        popups_closed += 1
        print("✅ Closed newsletter popup")
    except:
        pass

    # Try alternative selectors if needed
    if popups_closed == 0:
        print("⚠️ Trying alternative popup selectors...")
        alternative_selectors = [
            "button[data-dismiss='modal']",
            "button.close",
            "div.modal button.close"
        ]
        for selector in alternative_selectors:
            try:
                browser.find_element(By.CSS_SELECTOR, selector).click()
                popups_closed += 1
                print(f"✅ Closed popup using alternative: {selector}")
                break
            except:
                continue

    return popups_closed > 0

def get_price(num):
    global price_error
    browser = None
    try:
        browser = webdriver.Firefox(options=options)
        
        match num:
            # Pichau cases (0-3)
            case 0:
                component = "P - ASUS"
                browser.get('https://www.pichau.com.br/placa-de-video-asus-radeon-rx-7600-dual-evo-oc-edition-8gb-gddr6-128-bit-dual-rx7600-o8g-evo')
                price_selector = (By.CLASS_NAME, 'mui-1q2ojdg-price_vista')
            case 1:
                component = "P - XFX"
                browser.get('https://www.pichau.com.br/placa-de-video-xfx-radeon-rx-7600-speedster-swft210-8gb-gddr6-128-bit-rx-76pswftfy')
                price_selector = (By.CLASS_NAME, 'mui-1q2ojdg-price_vista')
            case 2:
                component = "P - ASROCK"
                browser.get('https://www.pichau.com.br/placa-de-video-asrock-radeon-rx-7600-challenger-oc-8gb-gddr6-128-bit-90-ga41zz-00uanf')
                price_selector = (By.CLASS_NAME, 'mui-1q2ojdg-price_vista')
            case 3:
                component = "P - GIGABYTE"
                browser.get('https://www.pichau.com.br/placa-de-video-gigabyte-radeon-rx-7600-gaming-oc-8gb-gddr6-128-bit-gv-r76gaming-oc-8gd')
                price_selector = (By.CLASS_NAME, 'mui-1q2ojdg-price_vista')
            
            # Terabyte cases (4-7) - ALL with popup handling
            case 4:
                component = "T - ASUS"
                browser.get('https://www.terabyteshop.com.br/produto/32738/placa-de-video-asus-dual-amd-radeon-rx-7600-evo-oc-edition-8gb-gddr6-fsr-ray-tracing-dual-rx7600-o8g-evo')
                close_terabyte_popups(browser)
                price_selector = (By.CLASS_NAME, 'valVista')
            case 5:
                component = "T - XFX"
                browser.get('https://www.terabyteshop.com.br/produto/25101/placa-de-video-xfx-amd-radeon-rx-7600-speedster-qick-308-8gb-gddr6-fsr-ray-tracing-rx-76pqickby')
                close_terabyte_popups(browser)
                price_selector = (By.CLASS_NAME, 'valVista')
            case 6:
                component = "T - ASROCK"
                browser.get('https://www.terabyteshop.com.br/produto/25051/placa-de-video-asrock-amd-radeon-rx-7600-challenger-oc-8gb-gddr6-fsr-ray-tracing-90-ga41zz-00uanf')
                close_terabyte_popups(browser)
                price_selector = (By.CLASS_NAME, 'valVista')
            case 7:
                component = "T - ASROCK (Steel Legend)"
                browser.get('https://www.terabyteshop.com.br/produto/25052/placa-de-video-asrock-amd-radeon-rx-7600-steel-legend-oc-8gb-gddr6-fsr-ray-tracing-90-ga4dzz-00uanf')
                close_terabyte_popups(browser)
                price_selector = (By.CLASS_NAME, 'valVista')
            case 8:
                component = "K - GIGABYTE"
                browser.get('https://www.kabum.com.br/produto/475647/placa-de-video-rx-7600-gaming-oc-8g-amd-radeon-gigabyte-8gb-gddr6-128bits-rgb-gv-r76gaming-oc-8gd')
                price_selector = (By.CLASS_NAME, 'finalPrice')
            case 9:
                component = "K - XFX"
                browser.get('https://www.kabum.com.br/produto/463543/placa-de-video-rx-7600-series-graphics-cards-xfx-amd-radeon-8gb-gddr6-rx-76pqickby')
                price_selector = (By.CLASS_NAME, 'finalPrice')
            case 10:
                component = "K - ASROCK (Steel Legend)"
                browser.get('https://www.kabum.com.br/produto/459143/placa-de-video-rx-7600-steel-legend-asrock-amd-radeon-8gb-gddr6-argb-90-ga4dzz-00uanf')
                price_selector = (By.CLASS_NAME, 'finalPrice')
            case 11:
                component = "K - ASROCK"
                browser.get('https://www.kabum.com.br/produto/573345/placa-de-video-challenger-asrock-amd-radeon-rx-7600-8gb-gddr6-128-bits-90-ga41zz-00uanf')
                price_selector = (By.CLASS_NAME, 'finalPrice')
        
        
        print(f"Accessing {component}...")
        time.sleep(2)

        try:
            price_element = WebDriverWait(browser, 15).until(
                EC.visibility_of_element_located(price_selector)
            )
            price_text = price_element.text
            
            if not price_text or "R$ 0,00" in price_text:
                raise ValueError("Invalid price format")
            
            price = (
                price_text.split()[1].replace(".","").replace(",",".")
                if "T - " in component
                else price_text.replace("R$","").strip().replace(".","").replace(",",".")
            )
            
            with open(filename, 'r') as file:
                data = json.load(file)
                previous_prices = data[component]
                
                # Check if we have any prices recorded today
                today_prices = [p for p in previous_prices if p['date'] == datetime.today().strftime('%Y-%m-%d')]
                
                if not today_prices:
                    # First run today - record initial price
                    new_entry = {"date": datetime.today().strftime('%Y-%m-%d'), "price": price}
                    data[component].append(new_entry)
                    with open(filename, 'w') as file:
                        json.dump(data, file, indent=4)
                    print(f"✅ Recorded today's initial price: {price}")
                    
                    # Notify if this is first ever recording or if dropped from yesterday
                    if previous_prices:
                        last_price = previous_prices[-1]['price']
                        if float(price) < float(last_price):
                            notify_discord(component, price, last_price)
                    else:
                        notify_discord(component, price)
                else:
                    # Subsequent run today - check for price drops
                    today_price = today_prices[-1]['price']
                    current_price_float = float(price)
                    recorded_price_float = float(today_price)
                    
                    if current_price_float < recorded_price_float:
                        # Price dropped - update record and notify
                        today_prices[-1]['price'] = price
                        with open(filename, 'w') as file:
                            json.dump(data, file, indent=4)
                        notify_discord(component, price, today_price)
                        print(f"⚠️ Price dropped from today's recorded price: {today_price} → {price}")
                    else:
                        # Price same or higher - no action needed
                        print(f"ℹ️ Current price ({price}) same or higher than today's recorded price ({today_price})")
            
        except Exception as e:
            print(f"❌ Failed to get price: {str(e)}")
            price_error += f"{component}, "
            browser.save_screenshot(f"error_{num}.png")
            
    finally:
        if browser:
            try:
                browser.quit()
            except:
                pass

today = datetime.today().strftime('%Y-%m-%d')

try:
    with open(filename, "r") as file:
        data = json.load(file)
except Exception as e:
    print(f"Error reading file: {str(e)}")
    exit()

# Always check all components when run (multiple times per day)
print("Checking all components for price drops...")
for i in range(component_num):
    get_price(i)
    
if price_error:
    print("PRICES WITH ERROR:", price_error)
