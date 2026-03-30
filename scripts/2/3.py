import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import par84

# === Export HTML avec par84 ===
images, config = par84.img_path + "3-", {'displayModeBar': True}

# === Subreddits officiels des cryptos ===
subreddits = {
    "Bitcoin": "Bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Litecoin": "litecoin",
    "Bitcoin Cash": "BitcoinCash",
    "Dogecoin": "dogecoin",
    "Cardano": "cardano",
    "Polygon": "MaticNetwork",
    "TRON": "TRON",
    "XRP": "ripple"
}

data = []

# === Récupération du nombre d'abonnés sur Reddit ===
for crypto, subreddit in subreddits.items():
    try:
        url = f"https://www.reddit.com/r/{subreddit}/about.json"
        headers = {"User-Agent": "CryptoPopularityScript/0.1"}
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            subscribers = 0
        else:
            info = res.json()
            subscribers = info["data"].get("subscribers", 0)

        data.append({"crypto": crypto, "subscribers": subscribers})
    
    except Exception as e:
        data.append({"crypto": crypto, "subscribers": 0})

df = pd.DataFrame(data)

# === Normalisation score 0-100 ===
min_val = df["subscribers"].min()
max_val = df["subscribers"].max()
df["score"] = ((df["subscribers"] - min_val) / (max_val - min_val) * 100) if max_val - min_val > 0 else 0

# === Bubble chart Plotly ===
fig = go.Figure(go.Scatter(
    x=df["crypto"],
    y=df["score"],
    mode='markers+text',
    text=df["crypto"],
    textposition='top center',
    marker=dict(
        size=df["subscribers"] / 10000,  # ajuster le facteur pour visibilité
        color=df["score"],
        colorscale='Viridis',
        showscale=True,
        sizemode='area',
        sizeref=2.*max(df["subscribers"] / 10000)/(100**2)
    )
))

fig.update_layout(
    title="Crypto Popularity on Reddit (Bubble Chart, normalized 0–100)",
    xaxis_title="Crypto",
    yaxis_title="Score /100",
    template="plotly_dark",
    height=500
)

# === Export HTML via par84 ===
plot(fig, filename=images + "1.html", config=config, auto_open=False)

# === Debug console ===
print(df[["crypto", "subscribers", "score"]])