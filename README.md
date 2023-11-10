# pyrice-logger
Price logger written in Python  
For now it's only suitable for my personal usage, but I'm constantly improving it.

### Python modules 
- Selenium
- Plotly

### How it works
By running `individual.py`, the script will search for the price for each item's hardcoded website by it's id using Selenium. The price will be parsed to become a float and it will be inserted into `individual_price.json` with today's date. 

In order to visualize the price history in a graph, run `individualgraph.py` and Plotly will display it in your browser.
