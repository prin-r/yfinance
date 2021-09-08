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

# US stock market hours
# The NYSE and the NASDAQ are the two largest American exchanges,
# both of which are located in New York City. Their regular stock
# trading hours are Monday to Friday 9:30 am to 4:30 pm EST (2:30pm to 9pm GMT).
# 2:30pm to 9pm GMT -> 14:30 to 21:00
def get_price(symbol):
    # if market is open then use "regularMarketPrice"
    # else use "preMarketPrice"

    # utc now
    now = datetime.datetime.utcnow()
    # 14:30
    open_time = datetime.datetime(now.year, now.month, now.day, 14, 30)
    # 21:00
    close_time = datetime.datetime(now.year, now.month, now.day, 21, 0)

    if now > open_time and now < close_time:
        return tickers.tickers[symbol].info["regularMarketPrice"]
    else:
        return tickers.tickers[symbol].info["preMarketPrice"]


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
