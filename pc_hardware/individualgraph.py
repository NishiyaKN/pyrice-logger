import json
import plotly.graph_objs as go

dates = [[],[],[],[],[]]
prices = [[],[],[],[],[]]

file = open("individual_price.json", "r")
file_data = json.load(file)
file.close()

for i in range(0,5):
    match i:
        case 0:
            component = "RX 6600"
        case 1:
            component = "RX 6500 XT"
        case 2:
            component = "5 5600"
        case 3:
            component = "5 5500"
        case 4:
            component = "5 4600G"
    data = file_data[component]

    dates[i] = [entry["date"] for entry in data]
    prices[i] = [entry["price"] for entry in data]
    prices[i] = [float(x) for x in prices[i]]

fig = go.Figure([
    go.Scatter(
        name='RX 6600',
        x=dates[0],
        y=prices[0],
        mode='markers+lines',
        marker=dict(color='#0400ff',size=2),
        showlegend=True
        ),
    go.Scatter(
        name='RX 6500 XT',
        x=dates[1],
        y=prices[1],
        mode='markers+lines',
        marker=dict(color='#00a6ff',size=2),
        showlegend=True
        ),
    go.Scatter(
        name='5 5600',
        x=dates[2],
        y=prices[2],
        mode='markers+lines',
        marker=dict(color='#ff000d',size=2),
        showlegend=True
        ),
    go.Scatter(
        name='5 5500',
        x=dates[3],
        y=prices[3],
        mode='markers+lines',
        marker=dict(color='#ff008c',size=2),
        showlegend=True
        ),
    go.Scatter(
        name='5 4600G',
        x=dates[4],
        y=prices[4],
        mode='markers+lines',
        marker=dict(color='#ff00ee',size=2),
        showlegend=True
        )
    ])

fig.update_layout(
    yaxis_range=[0,2000],
    yaxis_title="Price",
    xaxis_title="Day",
    title="Individual components price",
    )

fig.show()
