import yfinance as yf
import par84
import plotly.graph_objects as go
from plotly.offline import plot
import pandas as pd

# 🎯 10 cryptos
symbols = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "XRP": "XRP-USD",
    "LTC": "LTC-USD", "BCH": "BCH-USD", "ADA": "ADA-USD",
    "XLM": "XLM-USD", "TRX": "TRX-USD", "DASH": "DASH-USD", "ETC": "ETC-USD"
}

images = par84.img_path + '2-'

returns = pd.DataFrame()

# 📥 Téléchargement
for name, ticker in symbols.items():

    df = yf.Ticker(ticker).history(period='5y', auto_adjust=True)

    if not df.empty:
        returns[name] = df["Close"].pct_change()
        print(f"✅ {name}")

# Supprimer NaN
returns = returns.dropna()

# 📊 Matrice de corrélation
corr_matrix = returns.corr()

# 🎨 Heatmap
fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        text=corr_matrix.round(2),
        texttemplate="%{text}",
        colorbar=dict(title="Correlation")
))

fig.update_layout(
    title="Correlation Matrix - Crypto Portfolio (5 Years)",
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='white')
)

# 💾 sauvegarde
plot(fig, filename=images+'1.html', config=par84.config, auto_open=False)

print("✅ Matrice de corrélation terminée !")