import requests
import plotly.graph_objects as go
from plotly.offline import plot
import par84

images, config = par84.img_path+'1-', {'displayModeBar':True}

# mapping CoinMetrics
symbols = {
    'btc':'Bitcoin',
    'eth':'Ethereum',
    'ltc':'Litecoin',
    'bch':'Bitcoin Cash',
    'doge':'Dogecoin',
    'ada':'Cardano',
    'xrp':'XRP',
    'sol':'Solana',
    'matic':'Polygon',
    'trx':'TRON'
}

active_addresses = []

for s, name in symbols.items():
    try:
        url = "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics"
        params = {
            "assets": s,
            "metrics": "AdrActCnt",
            "frequency": "1d",
            "page_size": 1
        }

        r = requests.get(url, params=params)
        data = r.json()

        value = float(data['data'][0]['AdrActCnt'])
        active_addresses.append(value if value else 100_000)

        print(f"{name}: {int(value):,} active addresses")

    except:
        fallback = 100_000
        active_addresses.append(fallback)
        print(f"{name}: fallback → {fallback}")

# Plot (Treemap pour cohérence avec ton graph market cap)
fig = go.Figure(go.Treemap(
    labels=list(symbols.values()),
    parents=[""]*len(symbols),
    values=active_addresses,
    marker=dict(colors=[
        '#F7931A','#627EEA','#345D9D','#8DC351','#C2A633',
        '#0033AD','#00A8E8','#14F195','#8247E5','#FF0018'
    ]),
    textinfo="label+value",
    texttemplate="%{label}<br>%{value:,.0f}"
))

fig.update_layout(
    title="Active Addresses (On-chain Activity)",
    height=450,
    template='plotly_dark'
)

plot(fig, filename=images+'1.html', config=config, auto_open=False)