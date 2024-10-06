# collect_data.py
# Handles data scraping, API requests, and any other methods used to gather raw data

import requests
import json
import os
from dotenv import load_dotenv
from utils import ensure_dir, save_data

def fetch_market_data(path : str):
    coin_gecko_root_url = 'https://api.coingecko.com/api/v3/'
    COIN_GECKO_API_KEY = os.getenv('COIN_GECKO_API_KEY')
    headers = { 'x-cg-demo-api-key' : COIN_GECKO_API_KEY }
    queryParams = { 'vs_currency' : 'usd' }    
    
    
    r = requests.get(coin_gecko_root_url + path, headers=headers, params=queryParams)
    print(r.json())
    
    ensure_dir('./raw_data/market_data')
    save_data(r.json(), './raw_data/market_data/coins.json')

if __name__ == "__main__":
    load_dotenv()
    fetch_market_data('coins/markets')