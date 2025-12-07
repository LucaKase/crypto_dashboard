import requests

BASE_URL = "https://api.binance.com/api/v3"


def get_orderbook(symbol, limit=10):
    url = f"{BASE_URL}/depth"
    params = {"symbol": symbol.upper(), "limit": limit}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Orderbook REST error:", e)
        return None


def get_klines(symbol, interval="1m", limit=30):
    url = f"{BASE_URL}/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Kline REST error:", e)
        return None
