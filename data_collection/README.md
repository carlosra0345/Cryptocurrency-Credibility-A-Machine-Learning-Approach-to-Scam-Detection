## Data Collection

This folder contains all the scripts and configurations required for collecting raw data from various cryptocurrency-related APIs. The data collected will be used to train the machine learning model, which predicts the credibility of cryptocurrencies.

### Folder Contents:

- **`collect_data.py`**:  
  The main script responsible for retrieving cryptocurrency data from APIs like CoinGecko and storing it in the appropriate format (e.g., CSV or JSON).

- **`.env`**:  
  A file that contains sensitive environment variables such as API keys. This file should not be committed to version control (make sure it is listed in your `.gitignore`).

- **`requirements.txt`**:  
  A list of Python dependencies required for running the data collection script. Use the following command to install the necessary packages:

  ```bash
  pip install -r requirements.txt
  ```

### How to Run the Data Collection Script:

1. **Set up API Keys**:  
   - Ensure that you have an API key from the relevant data provider (e.g., CoinGecko, Etherscan).
   - Add your API key to the `.env` file in the following format:

     ```env
     COIN_GECKO_API_KEY=your_api_key_here
     ```

2. **Install Dependencies**:  
   Make sure all necessary dependencies are installed by running:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Script**:  
   Run the `collect_data.py` script to fetch the data:

   ```bash
   python collect_data.py
   ```

### Data Storage:

- By default, the script stores the raw data in the `data/` directory in **JSON** or **CSV** format, depending on your configuration.
- Ensure you have enough disk space, as cryptocurrency datasets can grow large over time.

### Important Notes:

- **Do not commit your `.env` file** to version control to avoid exposing sensitive API keys.
- Make sure to follow API rate limits to avoid being blocked by the data provider.

### Reproducibility of Data Collection:

While this folder contains all of the code required to reproduce the methods utilized in obtaining the data, there may be some discrepancies between the initial data collected (which was used to train the machine learning model) and the data you reproduce. This is due to the nature of the cryptocurrency market, where prices, volumes, and other statistics are volatile. 

Additionally, APIs may return updated or modified data based on new events, developments, token listings, or blockchain conditions.

Therefore, while the general methodology remains consistent, your dataset may not be identical to the one used in the original machine learning model training process.
