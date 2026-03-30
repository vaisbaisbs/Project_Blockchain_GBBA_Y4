import yfinance as yf
import par84
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
 
# 10 cryptos
symbols = {
    "BTC": "BTC-USD", "ETH": "ETH-USD", "XRP": "XRP-USD",
    "LTC": "LTC-USD", "BCH": "BCH-USD", "ADA": "ADA-USD",
    "XLM": "XLM-USD", "TRX": "TRX-USD", "DASH": "DASH-USD", "ETC": "ETC-USD"
}
 

images = par84.img_path + '5-'
 
# Load the data
returns = pd.DataFrame()
for name, ticker in symbols.items():
    df = yf.Ticker(ticker).history(period='5y', auto_adjust=True)
    if not df.empty:
        returns[name] = df["Close"].pct_change()
        print(f"✅ {name}")
returns = returns.dropna()
 
# Portfolio Simulation Monte Carlo
mean_returns = returns.mean()
cov_matrix = returns.cov()
num_portfolios = 50000
risk_free_rate = 0.03
 
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
 
# PLot the graph as a cloud of porfolios 
fig = go.Figure()
 
# cloud of porfolios 
scatter_all = go.Scatter(
    x=results_df['Volatility'],
    y=results_df['Return'],
    mode='markers',
    marker=dict(
        color=results_df['Sharpe'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Sharpe Ratio"),
        size=5,
        opacity=0.6
    ),
    name='Simulated Portfolio',
    hovertemplate='<b>Volatility:</b> %{x:.2%}<br><b>Return:</b> %{y:.2%}<br><extra></extra>'
)
fig.add_trace(scatter_all)
 
# Optiml portfolio(max Sharpe)
scatter_opt = go.Scatter(
    x=[max_sharpe_port['Volatility']],
    y=[max_sharpe_port['Return']],
    mode='markers+text',
    marker=dict(color='red', size=15, symbol='star', line=dict(color='white', width=2)),
    text=['Optimal'],
    textposition='top center',
    name='Optimal Portfolio (Max Sharpe)',
    hovertemplate='<b>Optimal Portfolio</b><br><b>Volatilité:</b> %{x:.2%}<br><b>Return:</b> %{y:.2%}<br><b>Sharpe:</b> ' + f'{max_sharpe_port["Sharpe"]:.2f}<extra></extra>'
)
fig.add_trace(scatter_opt)
 
# Layout
fig.update_layout(
    height=450,
    width=500,
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='white', size=12),
    title=dict(
        text="Efficient Frontier",
        font=dict(size=16, color='white')
    ),
    xaxis=dict(
        title='Annualized volatility',
        gridcolor='#333',
        showgrid=True
    ),
    yaxis=dict(
        title='Return annualized',
        gridcolor='#333',
        showgrid=True
    ),
    hovermode='closest',
    legend=dict(
        x=0.08,
        y=0.02,
        bgcolor='rgba(0,0,0,0.7)',
        bordercolor='white',
        borderwidth=1,
        font=dict(size=9)
    )
)
 
# Sauvegarde HTML
plot(fig, filename=images + '1.html', auto_open=False)
