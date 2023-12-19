# pyrice-logger
Price logger written in Python

Used to log the prices of products I'm interested in buying.  
Running on a Raspberry Pi Zero 2 with systemd services :D

### Python modules 
- Selenium
- Pandas
- Beautiful Soup 4
- Requests
- Plotly

### How it works
There is a directory for each product, and their script's implementation depends on it's needs.  
On asus, for example, the script is `asus.py`, and it needs Selenium in order to interact with the page: click to accept the cookies, scroll down the page and click the button to select the right specs with it's respective price. It then appends the new value with today's date to a .csv file and saves it. The file `asusgraph.py` uses the data from the .csv file to create a line graph with plotly, which will be displayed on your default browser. I have also made  systemd `asus.service` and `asus.timer` files to automatically run this script everyday at 6am. 
