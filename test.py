#!/usr/bin/env python3

from time import time
import concurrent.futures
import http.client
import sys
import json

SYMBOLS = [
    "AAPL",
    "GOOGL",
    "TSLA",
    "NFLX",
    "QQQ",
    "TWTR",
    "BABA",
    "IAU",
    "SLV",
    "USO",
    "VIXY",
    "AMZN",
    "MSFT",
    "FB",
    "GS",
    "ABNB",
    "GME",
    "AMC",
    "SPY",
    "COIN",
    "ARKK",
    "SQ",
    "AMD",
    "HOOD",
]

# REG_KEY = 'class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"'
# PRE_KEY = 'class="C($primaryColor) Fz(24px) Fw(b)"'

# def request_reg(symbol):
#     res = requests.get(URL.format(symbol, symbol))
#     tmp = res.text
#     tmp = tmp[tmp.index(REG_KEY) + len(REG_KEY) :]
#     start, end = (tmp.find(">") + 1, tmp.find("<"))
#     return float(tmp[start:end].replace(",", ""))


# def request_pre(symbol):
#     res = requests.get(URL.format(symbol, symbol))
#     tmp = res.text
#     tmp = tmp[tmp.index(PRE_KEY) + len(PRE_KEY) :]
#     start, end = (tmp.find(">") + 1, tmp.find("<"))
#     return float(tmp[start:end].replace(",", ""))


def get_price(symbol):
    conn = http.client.HTTPSConnection("query2.finance.yahoo.com")
    payload = ""
    headers = {"Content-Type": "application/json"}
    conn.request("GET", "/v8/finance/chart/" + symbol, payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read())
    meta = data["chart"]["result"][0]["meta"]
    regular_period = meta["currentTradingPeriod"]["regular"]
    (regular_time_start, regular_time_end) = (regular_period["start"], regular_period["end"])

    # utc now
    now = int(time())
    if now > int(regular_time_start) and now < int(regular_time_end):
        return meta["regularMarketPrice"]
    else:
        return meta["previousClose"]


def main():
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(SYMBOLS)) as executor:
        future_to_symbol = {executor.submit(get_price, symbol): symbol for (symbol) in SYMBOLS}
        for future in concurrent.futures.as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                results[symbol] = future.result()
            except Exception as exc:
                print(f"{symbol} generated an exception: {exc}")

    return results  # sorted(results.items())


if __name__ == "__main__":
    try:
        print(main(*sys.argv[1:]))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
