import plotly.express as px
import pandas as pd

filename='asushistory.csv'

dataframe = pd.read_csv(filename,index_col=0)
dataframe['Price'] = dataframe['Price'].astype(float)
print(dataframe)

fig = px.line(dataframe, x="Date", y="Price", title='Price history')
fig.update_layout(yaxis_range=[1000,4000])
fig.show()

