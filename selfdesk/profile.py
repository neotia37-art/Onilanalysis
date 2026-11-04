"""Live company profile for the ticker on screen. No stored IBD sheets."""
from __future__ import annotations

import http.cookiejar
import json
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import quote
from urllib.request import HTTPCookieProcessor, Request, build_opener, urlopen

_UA = {"User-Agent": "Mozilla/5.0"}
_KST = timezone(timedelta(hours=9))
_CRUMB = {"at": 0.0, "opener": None, "crumb": ""}
_CACHE: dict = {}


def clear_profile_cache() -> None:
    _CACHE.clear()


def _raw(value):
    if isinstance(value, dict):
        return value.get("raw", value.get("fmt"))
    return value


def _opener():
    now = time.time()
    if _CRUMB["opener"] and _CRUMB["crumb"] and now - _CRUMB["at"] < 1500:
        return _CRUMB["opener"], _CRUMB["crumb"]
    jar = http.cookiejar.CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar))
    try:
        opener.open(Request("https://fc.yahoo.com", headers=_UA), timeout=10).read()
    except Exception:
        pass
    crumb = opener.open(
        Request("https://query1.finance.yahoo.com/v1/test/getcrumb", headers=_UA),
        timeout=10,
    ).read().decode("utf-8").strip()
    if not crumb or " " in crumb or "<" in crumb:
        raise RuntimeError("야후 인증값을 받지 못했습니다.")
    _CRUMB.update({"at": now, "opener": opener, "crumb": crumb})
    return opener, crumb


def _chart_meta(symbol: str) -> dict:
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{quote(symbol, safe='')}?range=5d&interval=1d"
    )
    req = Request(url, headers=_UA)
    with urlopen(req, timeout=12) as res:
        body = json.loads(res.read().decode("utf-8"))
    result = ((body.get("chart") or {}).get("result") or [None])[0]
    if not result:
        raise RuntimeError(symbol)
    return result.get("meta") or {}


def resolve_symbol(ticker: str, market: str | None = None) -> str:
    text = str(ticker or "").strip().upper()
    if not text:
        raise RuntimeError("티커가 없습니다.")
    if text.endswith(".KS") or text.endswith(".KQ"):
        return text
    if market == "KR" or (text.isdigit() and len(text) == 6):
        last = None
        for suffix in (".KS", ".KQ"):
            try:
                _chart_meta(text + suffix)
                return text + suffix
            except Exception as exc:
                last = exc
        raise RuntimeError(f"{text} 한국 시세를 찾지 못했습니다: {last}")
    return text


def _pct(value):
    number = _raw(value)
    if number is None:
        return None
    number = float(number)
    if abs(number) <= 2:
        number *= 100.0
    return number


def _when(unix) -> str | None:
    unix = _raw(unix)
    if not unix:
        return None
    try:
        return datetime.fromtimestamp(int(unix), tz=timezone.utc).astimezone(_KST).strftime("%Y-%m-%d %H:%M KST")
    except Exception:
        return None


def fetch_profile(ticker: str, market: str | None = None) -> dict:
    key = f"{market}:{str(ticker).upper()}"
    hit = _CACHE.get(key)
    if hit and time.time() - hit["at"] < 1800:
        return hit["data"]
    symbol = resolve_symbol(ticker, market)
    meta = {}
    try:
        meta = _chart_meta(symbol)
    except Exception:
        meta = {}
    opener, crumb = _opener()
    modules = "assetProfile,financialData,defaultKeyStatistics,calendarEvents"
    url = (
        "https://query1.finance.yahoo.com/v10/finance/quoteSummary/"
        f"{quote(symbol, safe='')}?modules={modules}&crumb={quote(crumb)}"
    )
    raw = opener.open(Request(url, headers=_UA), timeout=12).read()
    result = ((json.loads(raw.decode("utf-8")).get("quoteSummary") or {}).get("result") or [None])[0]
    if not result:
        raise RuntimeError(f"{symbol} 회사 설명이 비어 있습니다.")
    profile = result.get("assetProfile") or {}
    financial = result.get("financialData") or {}
    stats = result.get("defaultKeyStatistics") or {}
    calendar = result.get("calendarEvents") or {}
    officers = profile.get("companyOfficers") or []
    ceo = None
    for officer in officers:
        title = str(officer.get("title") or "")
        if "CEO" in title.upper() or "Chief Executive" in title:
            ceo = officer.get("name")
            break
    if ceo is None and officers:
        ceo = officers[0].get("name")
    earnings = (calendar.get("earnings") or {}).get("earningsDate") or []
    earn_fmt = None
    if earnings:
        earn_fmt = earnings[0].get("fmt") or _when(earnings[0].get("raw"))
    summary = (profile.get("longBusinessSummary") or "").strip()
    data = {
        "symbol": symbol,
        "name": meta.get("longName") or meta.get("shortName") or symbol,
        "price": meta.get("regularMarketPrice"),
        "currency": meta.get("currency"),
        "quote_at": _when(meta.get("regularMarketTime")),
        "fetched_at": datetime.now(_KST).strftime("%Y-%m-%d %H:%M KST"),
        "summary": summary,
        "sector": profile.get("sector"),
        "industry": profile.get("industry"),
        "employees": _raw(profile.get("fullTimeEmployees")),
        "city": profile.get("city"),
        "country": profile.get("country"),
        "website": profile.get("website"),
        "ceo": ceo,
        "revenue_growth": _pct(financial.get("revenueGrowth")),
        "earnings_growth": _pct(financial.get("earningsGrowth")),
        "operating_margin": _pct(financial.get("operatingMargins")),
        "profit_margin": _pct(financial.get("profitMargins")),
        "roe": _pct(financial.get("returnOnEquity")),
        "debt_to_equity": _raw(financial.get("debtToEquity")),
        "short_pct": _pct(stats.get("shortPercentOfFloat")),
        "forward_pe": _raw(stats.get("forwardPE") or financial.get("forwardPE") or stats.get("trailingPE")),
        "peg": _raw(stats.get("pegRatio")),
        "next_earnings": earn_fmt[:10] if isinstance(earn_fmt, str) else None,
    }
    _CACHE[key] = {"at": time.time(), "data": data}
    return data
