import yfinance as yf
import par84
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd
import numpy as np

# 10 cryptos avec historique 5+ ans
symbols = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "XRP": "XRP-USD",
    "LTC": "LTC-USD",
    "BCH": "BCH-USD",
    "ADA": "ADA-USD",
    "XLM": "XLM-USD",
    "TRX": "TRX-USD",
    "DASH": "DASH-USD",
    "ETC": "ETC-USD"
}

images = par84.img_path + '1-'
data = {}

# paramètres
window = 90
risk_free = 0.02/252

# Charge the data
for name, ticker in symbols.items():

    df = yf.Ticker(ticker).history(period='5y', auto_adjust=True)

    if not df.empty:

        returns = df["Close"].pct_change()

        # downside returns
        downside = returns.copy()
        downside[downside > 0] = 0

        # rolling sortino
        expected_return = returns.rolling(window).mean()
        downside_std = np.sqrt((downside**2).rolling(window).mean())

        sortino = (expected_return - risk_free) / downside_std

        data[name] = sortino

        print(f"✅ {name}")

# Graphic ploting
fig = go.Figure()

for name, series in data.items():

    visible = True if name == "BTC" else "legendonly"

    fig.add_scatter(
        x=series.index,
        y=series,
        name=name,
        mode="lines",
        line=dict(width=2),
        visible=visible
    )

fig.update_layout(
    title="Sortino Ratio Rolling 90 days - 5 years",
    yaxis_title="Sortino Ratio",
    hovermode="x unified",
    showlegend=True,
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis=dict(gridcolor='gray', gridwidth=0.5),
    yaxis=dict(gridcolor='gray', gridwidth=0.5),
    annotations=[
        dict(
            x=0.5,
            y=-0.15,
            xref="paper",
            yref="paper",
            text="Click on any Crypto for specific data",
            showarrow=False,
            font=dict(color='yellow', size=12)
        )
    ]
)

# Save in html Iframe for the html pages
plot(fig, filename=images + '1.html', auto_open=False)

print("✅ Graph Sortino terminé !")