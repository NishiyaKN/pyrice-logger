import plotly.express as px
import json
import pandas as pd

file = open("price_history.json", "r")
data = json.load(file)

for item in data:
    item["price"] = float(item["price"])

df = pd.DataFrame(data)
fig = px.line(df, x="date", y="price", title='Price history')
fig.update_layout(yaxis_range=[1000,4000])
fig.show()
