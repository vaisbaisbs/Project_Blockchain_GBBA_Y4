import yfinance as yf
import par84
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot

# 🎯 10 cryptos
symbols = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "XRP": "XRP-USD",
    "LTC": "LTC-USD", "BCH": "BCH-USD", "ADA": "ADA-USD",
    "XLM": "XLM-USD", "TRX": "TRX-USD", "DASH": "DASH-USD", "ETC": "ETC-USD"
}

# 💾 chemin pour sauvegarde
images = par84.img_path + '6-'

# 📥 Téléchargement des prix et calcul des returns
prices = pd.DataFrame()
returns = pd.DataFrame()
for name, ticker in symbols.items():
    df = yf.Ticker(ticker).history(period='5y', auto_adjust=True)
    if not df.empty:
        prices[name] = df["Close"]
        returns[name] = df["Close"].pct_change()
returns = returns.dropna()

# 📊 Portefeuille optimal (par exemple calculé précédemment)
# Ici on reprend un portefeuille uniforme comme exemple
weights = np.array([0.2,0.2,0.1,0.1,0.1,0.05,0.05,0.05,0.05,0.1])
weights /= np.sum(weights)

# Rendement moyen et covariance du portefeuille
mean_returns = returns.mean()
cov_matrix = returns.cov()

# Paramètres simulation Monte Carlo
T = 252  # jours à simuler (~1 an)
dt = 1
n_sim = 500  # nombre de chemins simulés

# Rendement moyen et volatilité du portefeuille
port_mean = np.dot(weights, mean_returns)
port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

# Prix initial du portefeuille
port_initial = np.dot(prices.iloc[-1].values, weights)

# 🎯 Simulation des chemins GBM
simulations = np.zeros((T, n_sim))
for i in range(n_sim):
    S = port_initial
    path = [S]
    for t in range(1, T):
        Z = np.random.normal()
        S = path[-1] * np.exp((port_mean - 0.5*port_vol**2)*dt + port_vol*np.sqrt(dt)*Z)
        path.append(S)
    simulations[:, i] = path

# Calcul statistiques
final_values = simulations[-1, :]
VaR_5 = np.percentile(final_values, 5)
ES_5 = final_values[final_values <= VaR_5].mean()
min_val = simulations.min()
max_val = simulations.max()
mean_val = simulations.mean()

print(f"Portefeuille initial : {port_initial:.2f}")
print(f"Valeur min atteinte : {min_val:.2f}")
print(f"Valeur max atteinte : {max_val:.2f}")
print(f"Valeur finale moyenne : {mean_val:.2f}")
print(f"VaR 5% : {VaR_5:.2f}")
print(f"Expected Shortfall 5% : {ES_5:.2f}")

# 🎨 Graphique Monte Carlo
fig = go.Figure()

# Chemins simulés
for i in range(n_sim):
    fig.add_trace(go.Scatter(
        x=np.arange(T),
        y=simulations[:, i],
        mode='lines',
        line=dict(color='blue', width=1),
        opacity=0.1,
        showlegend=False
    ))

# Valeur moyenne
fig.add_trace(go.Scatter(
    x=np.arange(T),
    y=simulations.mean(axis=1),
    mode='lines',
    line=dict(color='yellow', width=3),
    name='Moyenne portefeuille'
))

# Valeur min/max
fig.add_trace(go.Scatter(
    x=np.arange(T),
    y=simulations.min(axis=1),
    mode='lines',
    line=dict(color='red', width=2, dash='dash'),
    name='Min portefeuille'
))
fig.add_trace(go.Scatter(
    x=np.arange(T),
    y=simulations.max(axis=1),
    mode='lines',
    line=dict(color='green', width=2, dash='dash'),
    name='Max portefeuille'
))

fig.update_layout(
    title="Simulation Monte Carlo - Portefeuille Crypto (GBM)",
    xaxis_title="Jours",
    yaxis_title="Valeur du portefeuille",
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='white')
)

plot(fig, filename=images+'1.html', auto_open=True)