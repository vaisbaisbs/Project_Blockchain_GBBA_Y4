import yfinance as yf
import par84
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot

# 🎯 10 cryptos
symbols = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "XRP": "XRP-USD",
    "LTC": "LTC-USD", "BCH": "BCH-USD", "ADA": "ADA-USD",
    "XLM": "XLM-USD", "TRX": "TRX-USD", "DASH": "DASH-USD", "ETC": "ETC-USD"
}

# 💾 chemin pour sauvegarde
images = par84.img_path + '5-'

# 📥 Téléchargement des prix et calcul des returns
returns = pd.DataFrame()
for name, ticker in symbols.items():
    df = yf.Ticker(ticker).history(period='5y', auto_adjust=True)
    if not df.empty:
        returns[name] = df["Close"].pct_change()
        print(f"✅ {name}")
returns = returns.dropna()

# 1️⃣ Simulation de portefeuilles pour Markowitz
mean_returns = returns.mean()
cov_matrix = returns.cov()
num_portfolios = 50000
risk_free_rate = 0.0

results = np.zeros((3+len(symbols), num_portfolios))
for i in range(num_portfolios):
    weights = np.random.random(len(symbols))
    weights /= np.sum(weights)
    port_return = np.dot(weights, mean_returns)*252
    port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix*252, weights)))
    sharpe_ratio = (port_return - risk_free_rate) / port_std
    results[0,i] = port_return
    results[1,i] = port_std
    results[2,i] = sharpe_ratio
    results[3:,i] = weights

results_df = pd.DataFrame(results.T, columns=['Return','Volatility','Sharpe'] + list(symbols.keys()))
max_sharpe_port = results_df.iloc[results_df['Sharpe'].idxmax()]

# 2️⃣ Création figure combinée (simulation + composition portefeuille)
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type":"scatter"}, {"type":"domain"}]],
    subplot_titles=("Frontière efficiente", "Composition du portefeuille optimal")
)

# Frontière efficiente
scatter_all = go.Scatter(
    x=results_df['Volatility'],
    y=results_df['Return'],
    mode='markers',
    marker=dict(color=results_df['Sharpe'], colorscale='Viridis', showscale=True, colorbar=dict(title="Sharpe")),
    name='Portefeuilles simulés'
)
fig.add_trace(scatter_all, row=1, col=1)

# Portefeuille optimal sur le scatter
scatter_opt = go.Scatter(
    x=[max_sharpe_port['Volatility']],
    y=[max_sharpe_port['Return']],
    mode='markers',
    marker=dict(color='red', size=12, symbol='star'),
    name='Portefeuille optimal (max Sharpe)'
)
fig.add_trace(scatter_opt, row=1, col=1)

# Pie chart composition portefeuille optimal
pie_weights = go.Pie(
    labels=list(symbols.keys()),
    values=max_sharpe_port[list(symbols.keys())]*100,
    textinfo='label+percent',
    marker=dict(colors=px.colors.qualitative.Vivid),
    name="Composition"
)
fig.add_trace(pie_weights, row=1, col=2)

# Layout général
fig.update_layout(
    height=600,
    width=1200,
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='white'),
    title_text="Analyse Portfolio Crypto - Markowitz",
    hovermode='closest'
)

# Sauvegarde HTML
plot(fig, filename=images + '1.html', auto_open=False)
print("✅ Analyse complète sauvegardée dans :", images + '1.html')