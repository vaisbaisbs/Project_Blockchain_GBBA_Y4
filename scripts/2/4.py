import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import par84

images, config = par84.img_path+'4-', {'displayModeBar':True}

symbols = {
    'btc':'Bitcoin',
    'eth':'Ethereum',
    'sol':'Solana',
    'ltc':'Litecoin',
    'bch':'Bitcoin Cash',
    'doge':'Dogecoin',
    'ada':'Cardano',
    'matic':'Polygon',
    'trx':'TRON',
    'xrp':'XRP'
}

fig = go.Figure()

for s, name in symbols.items():
    try:
        url = "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics"
        params = {
            "assets": s,
            "metrics": "TxCnt",
            "frequency": "1d",
            "page_size": 200
        }

        r = requests.get(url, params=params)
        data = r.json()['data']

        if not data:
            continue

        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'])
        df['TxCnt'] = pd.to_numeric(df['TxCnt'], errors='coerce')

        df = df.dropna()

        # smoothing
        df['MA7'] = df['TxCnt'].rolling(7).mean()

        fig.add_trace(go.Scatter(
            x=df['time'],
            y=df['MA7'],
            mode='lines',
            name=name,
            visible=True  # ou "legendonly"
        ))

        print(f"{name}: OK ({len(df)} points)")

    except Exception as e:
        print(f"{name}: error → {e}")

fig.update_layout(
    title="Daily Transactions (7d MA, Log Scale)",
    template='plotly_dark',
    height=450,
    xaxis_title="Date",
    yaxis_title="Transactions / day (log scale)",
    yaxis_type="log",  # 🔥 clé
    legend_title="Blockchain",
    hovermode="x unified"
)

plot(fig, filename=images+'1.html', config=config, auto_open=False)