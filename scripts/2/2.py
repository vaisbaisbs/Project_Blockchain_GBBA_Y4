import requests
from datetime import datetime, timezone
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
import par84

images = par84.img_path + "2-"

RPC_URLS = [
    "https://cloudflare-eth.com",
    "https://ethereum.publicnode.com",
]

N_BLOCKS = 50  # nombre de blocs à récupérer

def rpc(method, params=None):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}
    for _ in range(3):
        for url in RPC_URLS:
            r = requests.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if "result" in data:
                    return data["result"]
    raise Exception("RPC failed for all URLs")

def to_int(x):
    return int(x, 16)

# dernier bloc
latest = to_int(rpc("eth_blockNumber"))
print("Latest block:", latest)

# récupération des blocs
rows = []
for b in range(latest - N_BLOCKS + 1, latest + 1):
    block = rpc("eth_getBlockByNumber", [hex(b), False])
    rows.append({
        "time": pd.to_datetime(to_int(block["timestamp"]), unit="s", utc=True),
        "tx": len(block["transactions"]),
        "gas": to_int(block["gasUsed"]) / 1e6,  # M gas
        "base_fee": to_int(block["baseFeePerGas"]) / 1e9,  # Gwei
    })

df = pd.DataFrame(rows)

# -----------------------------
# Graph 1 : Tx count + Gas used
# -----------------------------
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Tx count
fig.add_scatter(
    x=df["time"],
    y=df["tx"],
    mode="lines+markers",
    name="Tx count",
    secondary_y=False,
    marker=dict(color="#627EEA")
)

# Gas used
fig.add_scatter(
    x=df["time"],
    y=df["gas"],
    mode="lines+markers",
    name="Gas used (M)",
    secondary_y=True,
    marker=dict(color="#F7931A")
)

fig.update_layout(
    title="Ethereum – Last Blocks Activity",
    template='plotly_dark',
    height=450,
    hovermode="x unified"
)
fig.update_yaxes(title_text="Tx count", secondary_y=False)
fig.update_yaxes(title_text="Gas used (millions)", secondary_y=True)

# export HTML avec plot()
plot(fig, filename=images + "1.html", config=par84.config, auto_open=False)

