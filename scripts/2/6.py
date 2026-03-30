import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import par84

# === Export HTML avec par84 ===
images, config = par84.img_path + "6-", {'displayModeBar': True}

# === Repos GitHub des cryptos ===
repos = {
    "Bitcoin": "bitcoin/bitcoin",
    "Ethereum": "ethereum/go-ethereum",
    "Solana": "solana-labs/solana",
    "Litecoin": "litecoin-project/litecoin",
    "Bitcoin Cash": "bitcoin-cash-node/bitcoin-cash-node",
    "Dogecoin": "dogecoin/dogecoin",
    "Cardano": "input-output-hk/cardano-node",
    "Polygon": "maticnetwork/bor",
    "TRON": "tronprotocol/java-tron",
    "XRP": "XRPLF/rippled"
}

# === Token GitHub (recommandé pour éviter limite 60 req/h) ===
GITHUB_TOKEN = "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"  # Remplace par ton token personnel
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}

data = []

# === Récupération des données GitHub ===
for name, repo in repos.items():
    url = f"https://api.github.com/repos/{repo}"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        print(f"Erreur pour {name}: {res.status_code}")
        continue

    repo_data = res.json()

    data.append({
        "crypto": name,
        "stars": repo_data.get("stargazers_count", 0),
        "forks": repo_data.get("forks_count", 0),
        "issues": repo_data.get("open_issues_count", 0)
    })

# === Création DataFrame ===
df = pd.DataFrame(data)

# === Normalisation min-max pour chaque métrique ===
for col in ["stars", "forks", "issues"]:
    min_val = df[col].min()
    max_val = df[col].max()
    if max_val - min_val > 0:
        df[col + "_score"] = (df[col] - min_val) / (max_val - min_val) * 100
    else:
        df[col + "_score"] = 0  # si toutes les valeurs sont égales

# === Score global pondéré sur 100 ===
# Pondération : stars 40%, forks 35%, issues 25% (modifiable)
df["score"] = (
    df["stars_score"] * 0.4 +
    df["forks_score"] * 0.35 +
    df["issues_score"] * 0.25
)

# === Tri par score global ===
df = df.sort_values(by="score", ascending=False)

# ------------------ PLOT ------------------
fig = go.Figure(go.Bar(
    x=df["crypto"],
    y=df["score"],
    text=df["score"].round(2),
    textposition='auto',
    marker_color=[
        '#F7931A','#627EEA','#345D9D','#8DC351','#C2A633',
        '#0033AD','#00A8E8','#8247E5','#1F8ACB','#E84142'
    ]
))

fig.update_layout(
    title="Crypto GitHub Activity Score (stars, forks, issues)",
    xaxis_title="Crypto",
    yaxis_title="Score /100",
    template="plotly_dark",
    height=450,
    width=500
)

# === Export HTML via par84 ===
plot(fig, filename=images + "1.html", config=config, auto_open=False)

# === Debug console ===
print(df[["crypto", "stars_score", "forks_score", "issues_score", "score"]])