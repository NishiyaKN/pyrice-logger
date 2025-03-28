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
import os

# Configurable base path after home directory
HOME = os.path.expanduser('~')
RELATIVE_BASE = "re/git/pyrice-logger/gpu"  # Change this to your path

# Full configuration paths
BASE_PATH = os.path.join(HOME, RELATIVE_BASE)
PRODUCTS_FILE = os.path.join(BASE_PATH, "products.json")
PRICES_FILE = os.path.join(BASE_PATH, "price.json")
AUTH_FILE = os.path.join(HOME, ".config/tk/dc")  # This stays in standard location

# Initialize JSON files
try:
    with open(PRODUCTS_FILE) as f:
        products = json.load(f)['products']
    print(f"Loaded {len(products)} products from {PRODUCTS_FILE}")
except FileNotFoundError:
    print(f"Error: {PRODUCTS_FILE} not found")
    exit()

try:
    with open(PRICES_FILE, "x") as f:
        json.dump({p['name']: [] for p in products}, f, indent=4)
    print(f"Created new {PRICES_FILE}")
except FileExistsError:
    print(f"{PRICES_FILE} already exists")

# Browser setup
options = Options()
options.add_argument("--headless")
price_error = ""

def close_terabyte_popups(browser):
    """Handles Terabyte popups"""
    try:
        try:
            WebDriverWait(browser, 3).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='modal']"))
            )
            browser.find_element(By.CSS_SELECTOR, "button.tsG0HQh7bcmTha7pyanx-btn-close").click()
            browser.switch_to.default_content()
        except:
            pass
        
        browser.find_element(By.CSS_SELECTOR, "span.fa-times").click()
    except:
        pass

def notify_discord(component, new_price, old_price=None):
    """Send price alerts to Discord"""
    try:
        with open(AUTH_FILE) as f:
            token = f.read().strip()
        
        if old_price:
            change = float(new_price) - float(old_price)
            message = (
                f"🔻 Price drop for {component}\n"
                f"Was: R$ {old_price}\n"
                f"Now: R$ {new_price}\n"
                f"Saved: R$ {abs(change):.2f} ({abs(change)/float(old_price)*100:.1f}%)"
            )
        else:
            message = f"📊 New tracking for {component}: R$ {new_price}"
            
        requests.post(
            "https://discord.com/api/v9/channels/1180832500403155095/messages",
            json={"content": message},
            headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"}
        )
    except Exception as e:
        print(f"Discord error: {str(e)}")

def parse_selector(selector_str):
    """Convert 'TYPE:value' to Selenium locator"""
    try:
        selector_type, value = selector_str.split(':', 1)
        return (getattr(By, selector_type), value)
    except:
        raise ValueError(f"Invalid selector format: {selector_str}")

def get_price(product):
    global price_error
    browser = None
    try:
        print(f"\n🔍 Checking {product['name']}...")
        browser = webdriver.Firefox(options=options)
        browser.get(product['url'])
        
        if 'popup_handler' in product:
            globals()[product['popup_handler']](browser)
        
        locator_type, locator_value = parse_selector(product['price_selector'])
        price_element = WebDriverWait(browser, 15).until(
            EC.visibility_of_element_located((locator_type, locator_value))
        )
        price_text = price_element.text
        
        if not price_text or "R$ 0,00" in price_text:
            raise ValueError("Invalid price format")
        
        current_price = (
            price_text.split()[1].replace(".","").replace(",",".")
            if "T - " in product['name']
            else price_text.replace("R$","").strip().replace(".","").replace(",",".")
        )
        print(f"  ✅ Current price: R$ {current_price}")

        with open(PRICES_FILE, 'r+') as f:
            data = json.load(f)
            price_history = data[product['name']]
            today = datetime.today().strftime('%Y-%m-%d')
            
            # Find today's entry if it exists
            today_entry = next((p for p in price_history if p['date'] == today), None)
            
            if not today_entry:
                # First check today - create new entry
                print("  📅 First check today")
                previous_price = price_history[-1]['price'] if price_history else None
                
                new_entry = {"date": today, "price": current_price}
                data[product['name']].append(new_entry)
                
                # Notify if price dropped from previous recording
                if previous_price and float(current_price) < float(previous_price):
                    print(f"  ⬇️ Price drop from last recording! (Was: R$ {previous_price})")
                    notify_discord(product['name'], current_price, previous_price)
                elif not price_history:
                    notify_discord(product['name'], current_price)
                
            else:
                # Subsequent check today
                recorded_price = today_entry['price']
                if float(current_price) < float(recorded_price):
                    print(f"  ⬇️ Price drop detected today! (Was: R$ {recorded_price})")
                    # Store old price before updating
                    old_price = recorded_price
                    today_entry['price'] = current_price
                    notify_discord(product['name'], current_price, old_price)
                else:
                    print("  ➖ Price unchanged or higher today")
            
            # Write back to file
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            
    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
        price_error += f"{product['name']}, "
    finally:
        if browser:
            browser.quit()

# Main execution
if __name__ == '__main__':
    print(f"Starting price check at {datetime.now()}")
    for product in products:
        print(f"\n🔍 Trying to get product: {product['name']}")  # Added this line
        get_price(product)
    
    if price_error:
        print("\n❌ Failed components:", price_error)
    print("\n✅ Price check complete")
