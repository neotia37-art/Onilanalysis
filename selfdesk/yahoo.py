"""Daily bars from the public chart endpoint. Adjusted when a split factor exists."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.parse import quote as urlquote
from urllib.request import Request, urlopen


def fetch_daily(symbol: str, range_: str = "1y") -> list[dict]:
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{urlquote(symbol, safe='')}?range={range_}&interval=1d&includeAdjustedClose=true"
    )
    req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urlopen(req, timeout=12) as res:
        body = json.loads(res.read().decode("utf-8"))
    result = (body.get("chart") or {}).get("result") or [None]
    result = result[0]
    if not result:
        err = ((body.get("chart") or {}).get("error") or {}).get("description") or "empty"
        raise RuntimeError(f"{symbol}: {err}")
    ts = result.get("timestamp") or []
    quote = (result.get("indicators") or {}).get("quote") or [{}]
    quote = quote[0]
    adj = ((result.get("indicators") or {}).get("adjclose") or [{}])[0].get("adjclose") or []
    bars = []
    for i, unix in enumerate(ts):
        close = (quote.get("close") or [None])[i]
        high = (quote.get("high") or [None])[i]
        low = (quote.get("low") or [None])[i]
        open_ = (quote.get("open") or [None])[i]
        vol = (quote.get("volume") or [None])[i]
        if close is None or high is None or low is None or not close > 0:
            continue
        ratio = 1.0
        if i < len(adj) and adj[i] and close:
            ratio = adj[i] / close
        date = datetime.fromtimestamp(unix, tz=timezone.utc).strftime("%Y-%m-%d")
        bars.append(
            {
                "date": date,
                "open": (open_ or close) * ratio,
                "high": high * ratio,
                "low": low * ratio,
                "close": close * ratio,
                "volume": vol or 0,
            }
        )
    if len(bars) < 30:
        raise RuntimeError(f"{symbol}: not enough bars")
    return bars
