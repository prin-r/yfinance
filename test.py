#!/usr/bin/env python3

import datetime
import concurrent.futures
import yfinance as yf
import sys

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

tickers = yf.Tickers(" ".join(SYMBOLS))

def get_price(symbol):
    # if market is open then use "regularMarketPrice"
    # else use "preMarketPrice"
    return tickers.tickers[symbol].info["regularMarketPrice"]


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

    return results


if __name__ == "__main__":
    try:
        print(main(*sys.argv[1:]))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
