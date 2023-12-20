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

On `asus`, for example, the main script is `asus.py`, and it needs `selenium` in order to interact with the page: click to accept the cookies, scroll down the page and click the button to select the right specs with it's respective price. With `bs4` I'm able to parse the html and find the element containing the price. It then transforms the new price and today's date into a `pandas` dataframe and appends it to a .csv file containing prices from past days. If the new price is different than the last one recorded, then it sends a notification to discord with `requests`. The file `asusgraph.py` uses the data from the .csv file to create a line graph with `plotly`, which will be displayed on your default browser. I have also made a systemd `asus.service` and `asus.timer` file to automatically run this script everyday at 6am. 

The `pc` and `pc_hardware` directories also use `selenium`, but saves the information to a .json file. Future scripts will follow `asus` template. 
