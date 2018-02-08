import datetime
import requests

import pandas as pd


def nmr_at_addr(addr_str):
    "Number of NMR (float) at given address."
    url = 'https://api.etherscan.io/api?module=account&action=tokenbalance&'
    url += 'contractaddress=0x1776e1F26f98b1A5dF9cD347953a26dd3Cb46671&'
    url += 'address=%s'
    r = requests.get(url % addr_str)
    data = r.json()
    nmr = int(data['result']) / 1e18
    return nmr


def token_price_data(ticker='nmr'):
    "Price (and return) information for given ticker."
    tickers = {'nmr': 'numeraire',
               'btc': 'bitcoin',
               'eth': 'ethereum',
               'ltc': 'litecoin'}
    if ticker in tickers:
        ticker = tickers[ticker]
    url = 'https://api.coinmarketcap.com/v1/ticker/%s/' % ticker
    r = requests.get(url)
    data = r.json()[0]
    price = {}
    price['name'] = ticker
    price['price'] = float(data['price_usd'])
    price['ret1h'] = float(data['percent_change_1h']) / 100.0
    price['ret1d'] = float(data['percent_change_24h']) / 100.0
    price['ret7d'] = float(data['percent_change_7d']) / 100.0
    price['date'] = datetime.datetime.fromtimestamp(int(data['last_updated']))
    return price


def historical_prices(ticker):
    "Historical daily price as a dataframe with date as index"
    tickers = {'nmr': 'currencies/numeraire',
               'btc': 'currencies/bitcoin',
               'eth': 'currencies/ethereum',
               'ltc': 'currencies/litecoin',
               'mkt': 'global/marketcap-total'}
    url = 'https://graphs2.coinmarketcap.com/%s'
    r = requests.get(url % tickers[ticker])
    data = r.json()
    if ticker == 'mkt':
        data = data['market_cap_by_available_supply']
    else:
        data = data['price_usd']
    dates = []
    prices = []
    for date, price in data:
        d = datetime.datetime.fromtimestamp(date / 1e3)
        dates.append(d)
        prices.append(price)
    prices = pd.DataFrame(data=prices, columns=['usd'], index=dates)
    return prices
