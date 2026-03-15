import yfinance as yf
import par84
import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np

# 🎯 10 cryptos
symbols = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "XRP": "XRP-USD",
    "LTC": "LTC-USD", "BCH": "BCH-USD", "ADA": "ADA-USD",
    "XLM": "XLM-USD", "TRX": "TRX-USD", "DASH": "DASH-USD", "ETC": "ETC-USD"
}

images = par84.img_path + '4-'
data = {}

# 📥 Téléchargement
for name, ticker in symbols.items():
    df = yf.Ticker(ticker).history(period='5y', auto_adjust=True)
    if not df.empty:
        # Calcul des daily returns
        daily_returns = df["Close"].pct_change() * 100
        
        # Volatilité = écart-type mobile sur 30 jours (annualisée * sqrt(365) pour être parlant)
        volatility = daily_returns.rolling(30).std() * np.sqrt(365)
        
        data[name] = volatility
        print(f"✅ {name}")

# 🎨 Graphique
fig = go.Figure()

for name, series in data.items():
    # BTC visible, les autres dans la légende seulement
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
    title="Volatilité annualisée (rolling 30 jours) - 5 ans",
    yaxis_title="Volatilité annualisée (%)",
    xaxis_title="Date",
    hovermode="x unified",
    showlegend=True,
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='white'),
    # Annotation pour guider
    annotations=[
        dict(
            x=0.5,
            y=-0.15,
            xref="paper",
            yref="paper",
            text="💡 Cliquez sur les cryptos dans la légende pour les afficher",
            showarrow=False,
            font=dict(color='yellow', size=12)
        )
    ]
)

# 💾 Sauvegarde
plot(fig, filename=images+'1.html', config=par84.config, auto_open=False)
print("✅ Graphique de volatilité sauvegardé !")