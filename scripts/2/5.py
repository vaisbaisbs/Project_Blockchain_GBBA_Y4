import requests
from datetime import datetime, timezone
import plotly.graph_objects as go
from plotly.offline import plot
import par84

images = par84.img_path + "5-"

# nombre de blocs à afficher
N = 10
URL = "https://mempool.space/api/v1/blocks"
blocks = requests.get(URL).json()[:N]

# listes pour les données
heights = []
times = []
tx_counts = []

# récupération des données
for block in blocks:
    heights.append(block["height"])
    times.append(datetime.fromtimestamp(block["timestamp"], tz=timezone.utc))
    tx_counts.append(block["tx_count"])

# création figure
fig = go.Figure()

# ajout scatter
fig.add_trace(go.Scatter(
    x=heights,
    y=times,
    mode="markers",
    marker=dict(
        size=[(c ** 0.5)*2 for c in tx_counts],  # taille ajustée
        color="#F7931A",  # couleur Bitcoin orange
        opacity=0.8,
        line=dict(width=1, color="white")
    ),
    customdata=tx_counts,
    hovertemplate="Height: %{x}<br>Time: %{y}<br>Tx: %{customdata}<extra></extra>"
))

# layout avec template plotly_dark
fig.update_layout(
    title="Bitcoin – Last Blocks",
    xaxis_title="Block Height",
    yaxis_title="Timestamp (UTC)",
    template='plotly_dark',
    height=430,
    width=550,  
    hovermode="closest"
)

# export HTML
plot(fig, filename=images + "1.html", config=par84.config, auto_open=False)