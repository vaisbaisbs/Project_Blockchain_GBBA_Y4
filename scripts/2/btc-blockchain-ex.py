import requests
from datetime import datetime, timezone
import plotly.graph_objects as go
from plotly.offline import plot
import par84

images = par84.img_path + "btc-blockchain-"

URL = "https://mempool.space/api/v1/blocks"
N = 10
blocks = requests.get(URL).json()[:N]
#print(blocks)
heights = []
times = []
tx_counts = []

for block in blocks:
    heights.append(block["height"])
    times.append(datetime.fromtimestamp((block["timestamp"]), tz=timezone.utc))
    tx_counts.append(block["tx_count"])
    
fig = go.Figure(layout=par84.layout)
fig.add_scatter(
    x=heights,
    y=times,
    mode="markers",
    marker=dict(size=[(c ** 0.5) for c in tx_counts]),
    customdata=tx_counts,
    hovertemplate="%{y} <br> Tx %{customdata}<extra></extra>"
)
fig.update_layout(title="Bitcoin – last blocks", xaxis_title="Height", yaxis_title="Time")
plot(fig, filename=images + "1.html", config=par84.config, auto_open=False)


