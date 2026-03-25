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
images = par84.img_path + '3-'
 
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
 
# 2️⃣ Créer le pie chart de composition
# Filtrer les poids > 0.1% pour plus de clarté
weights_dict = {crypto: max_sharpe_port[crypto]*100 for crypto in symbols.keys()}
weights_sorted = sorted(weights_dict.items(), key=lambda x: x[1], reverse=True)
 
labels = [item[0] for item in weights_sorted]
values = [item[1] for item in weights_sorted]
 
# Couleurs Vivid pour le pie chart
colors = [
    '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A',
    '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'
]
 
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    textinfo='label+percent',
    textposition='inside',
    hovertemplate='<b>%{label}</b><br>Poids: %{value:.2f}%<extra></extra>',
    marker=dict(
        colors=colors[:len(labels)],
        line=dict(color='white', width=2)
    )
)])
 
fig.update_layout(
    height=400,
    width=450,
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='white', size=12),
    title=dict(
        text="Composition du Portefeuille Optimal ⭐<br><sub>Volatilité: {:.2%} | Return: {:.2%} | Sharpe: {:.2f}</sub>".format(
            max_sharpe_port['Volatility'],
            max_sharpe_port['Return'],
            max_sharpe_port['Sharpe']
        ),
        font=dict(size=16, color='white')
    ),
    showlegend=True,
    legend=dict(
        x=1.0,
        y=1.0,
        bgcolor='rgba(0,0,0,0.5)',
        bordercolor='white',
        borderwidth=1
    )
)
 
# Sauvegarde HTML
plot(fig, filename=images + '1.html', auto_open=False)

for crypto, weight in weights_sorted:
    if weight > 0.1:  # Afficher seulement les poids > 0.1%
        print(f"   {crypto:6} : {weight:6.2f}%")