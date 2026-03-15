import yfinance as yf
import par84
import plotly.graph_objects as go
from plotly.offline import plot

# 🎯 10 cryptos
symbols = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "XRP": "XRP-USD",
    "LTC": "LTC-USD", "BCH": "BCH-USD", "ADA": "ADA-USD",
    "XLM": "XLM-USD", "TRX": "TRX-USD", "DASH": "DASH-USD", "ETC": "ETC-USD"
}

images = par84.img_path + '3-'
data = {}

# 📥 Téléchargement dernier mois
for name, ticker in symbols.items():
    df = yf.Ticker(ticker).history(period='1mo', auto_adjust=True)
    if not df.empty:
        # Base 100 sur le premier jour du mois
        base100 = (df["Close"] / df["Close"].iloc[0]) * 100
        data[name] = base100
        print(f"✅ {name}")

# 🎨 Graphique
fig = go.Figure()

for name, series in data.items():
    # BTC visible, les autres dans la légende seulement
    visible = True if name == "BTC" else "legendonly"  # ⭐ BTC visible, autres cachées
    
    fig.add_scatter(
        x=series.index,
        y=series,
        name=name,
        mode="lines",
        line=dict(width=2),
        visible=visible
    )

fig.update_layout(
    title="Performance relative - Dernier Mois (Base 100)",
    yaxis_title="Performance (Base 100)",
    xaxis_title="Date",
    hovermode="x unified",
    showlegend=True,
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='white'),
  
)

# 💾 Sauvegarde
plot(fig, filename=images+'1.html', config=par84.config, auto_open=False)
print("✅ Terminé !")