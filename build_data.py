import io, json, urllib.request
import pandas as pd

def fred(series):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    raw = urllib.request.urlopen(url, timeout=60).read().decode()
    s = pd.read_csv(io.StringIO(raw), parse_dates=[0], index_col=0, na_values=".").iloc[:, 0].dropna()
    return s[s.index >= "1990-01-01"]

tp, y10, mort = fred("THREEFYTP10"), fred("DGS10"), fred("MORTGAGE30US")
daily = pd.concat({"tp": tp, "y": y10}, axis=1).dropna()

out = {
    "updated": str(daily.index.max().date()),
    "daily": {
        "d": [d.strftime("%Y-%m-%d") for d in daily.index],
        "tp": [round(v, 4) for v in daily["tp"]],
        "y": [round(v, 2) for v in daily["y"]],
    },
    "mortgage": {
        "d": [d.strftime("%Y-%m-%d") for d in mort.index],
        "r": [round(v, 2) for v in mort],
    },
}
with open("data.json", "w") as f:
    json.dump(out, f, separators=(",", ":"))
print(out["updated"], len(daily), len(mort))
