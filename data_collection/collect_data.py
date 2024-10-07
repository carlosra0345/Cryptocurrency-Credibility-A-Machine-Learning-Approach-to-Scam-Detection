import requests
import os
import time
from datetime import datetime
import json
from dotenv import load_dotenv
from utils import ensure_dir, save_data, check_directory_file_exists, load_data

COINGECKO_API_RATE_LIMIT = 30 # CoinGecko's demo API rate limits to 30 API calls per minute
MAX_RETRIES = 5

def fetch_all_coins(root_url : str, headers : dict) -> str:
    print('Fetching all supported coin id\'s from the CoinGecko API...')
    queryParams = { 'include_platform': 'true' }   
     
    res = requests.get(root_url + 'coins/list', headers=headers, params=queryParams)
    res.raise_for_status()
    
    directory_path = './raw_data/'
    file_name = 'coingecko_coin_list.json'
    ensure_dir(directory_path)
    save_data(res.json(), directory_path + file_name)
    print(f'Successfully saved coin id\'s to {directory_path + file_name}')
    print('------------------------------------------------------')
    
    return directory_path + file_name
    
def fetch_individual_coin_market_data(root_url : str, coin_id : str, headers : dict) -> any:
    queryParams = {
        'localization': 'false',
        'tickers': 'true',
        'market_data': 'true',
        'community_data': 'true',
        'developer_data': 'true',
    }
    endpoint_path = 'coins/' + coin_id
    res = requests.get(root_url + endpoint_path, headers = headers, params=queryParams)
    res.raise_for_status()
    
    return res.json()

def save_data_partial_jsonl(coin_data_list : list[dict], directory_path : str,  file_name : str) -> None:
    """
    Save data incrementally in JSON Lines format (each object on a new line).
    Appends each data entry as a new line to avoid loading large files into memory.
    """
    ensure_dir(directory_path)
    file_path = directory_path + file_name
    with open(file_path, 'a') as file:
        for coin_data in coin_data_list:
            file.write(json.dumps(coin_data) + ',\n')
                

def fetch_all_coin_market_data(coin_input_list_filepath: str, root_url: str, headers: dict) -> None:
    check_directory_file_exists(coin_input_list_filepath, f'{coin_input_list_filepath} does not exist. Unable to read coin data.')
    coin_list = load_data(coin_input_list_filepath)
    coin_data_list = []
    output_directory = './raw_data/market_data/'
    output_file = 'coingecko_market_data.json'
    
    # open JSON array object
    ensure_dir(output_directory)
    with open(output_directory + output_file, 'w') as file:
        file.write('[\n') 
    
    # Track the start time of each batch of 30 requests
    batch_size = 30
    request_count = 0
    start_time = datetime.now()
    max_retries = 3  # Maximum retry attempts in case of errors
    num_coins_attempted = 0

    for index, coinObj in enumerate(coin_list):
        coin_name = coinObj['name']
        num_coins_attempted += 1
        if coinObj['id'] == 'percy':
            break

        for retry_attempt in range(max_retries):
            try:
                print(f'Fetching data for {coin_name} (Attempt {retry_attempt + 1})... ')
                coin_data = fetch_individual_coin_market_data(root_url, coinObj['id'], headers)
                coin_data_list.append(coin_data)
                print('Success!')
                print('---------')
                
                request_count += 1
                break 

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429 or e.response.status_code == 500 or e.response.status_code == 503:
                    print(f'Retryable due to HTTP Error {e.response.status_code} for {coin_name}.')
                else:
                    print(f'Non-retryable HTTP Error {e.response.status_code} for {coin_name}: {e}')
                    break
            except requests.exceptions.ConnectionError:
                print(f'Connection error for {coin_name}. Retrying...')
            except Exception as e:
                print(f'Failed fetching {coin_name} data: {e}')
                break

            time.sleep(2 ** retry_attempt + 1)  # Exponential backoff
            
            # If max retries reached, log and continue to the next coin
            if retry_attempt == max_retries - 1:
                print(f'Failed to fetch data for {coin_name} after {max_retries} attempts.')
                print('-----------')

        # Save data after each batch
        if request_count >= batch_size:
            time_elapsed = (datetime.now() - start_time).total_seconds()
            if time_elapsed < 60:
                sleep_time = 60 - time_elapsed
                print(f'Sleeping for {sleep_time:.2f} seconds to avoid API rate limit...')
                time.sleep(sleep_time)
            
            # Save partial results after each batch
            print('Saving partial results...')
            save_data_partial_jsonl(coin_data_list, output_directory, output_file)
            coin_data_list.clear() 
            
            # Reset for the next batch
            request_count = 0
            start_time = datetime.now()
    
    # Save any remaining data that wasn't saved yet
    if coin_data_list:
        print('Saving remaining data...')
        save_data_partial_jsonl(coin_data_list, output_directory, output_file)
        
    with open(output_directory + output_file, 'a') as file:
        file.write(']\n') 


if __name__ == "__main__":
    try:
        load_dotenv()
        coin_gecko_root_url = 'https://api.coingecko.com/api/v3/'
        COIN_GECKO_API_KEY = os.getenv('COIN_GECKO_API_KEY')
        headers = { 'x-cg-demo-api-key' : COIN_GECKO_API_KEY }
        # coin_input_list_filepath = fetch_all_coins(coin_gecko_root_url, headers)
        # get_all_coin_market_data()
        
        coin_input_list_filepath = './raw_data/coingecko_coin_list.json'
        # fetch_all_coin_market_data(coin_input_list_filepath, coin_gecko_root_url, headers)
            
    except Exception as e:
        print(e)