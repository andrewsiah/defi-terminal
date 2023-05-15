# Takes in most recent transactions from a lp address
# turns it into a dataframe
# filters for those who's address are in a list of addresses
# returns that dataframe with the filtered transactions

import pandas as pd
import asyncio
import json
import time

from aioetherscan import Client
from asyncio_throttle import Throttler
import streamlit as st

async def get_smartwallet_df(contract_name, token_address):
    def load_labels_to_df(filepath) -> pd.DataFrame:
        # # Load the JSON data from a file into a string
        with open(filepath, 'r') as f:
            json_string = f.read()

        # Load the JSON data into a dictionary
        data_dict = json.loads(json_string)

        # Create a DataFrame from the dictionary
        return pd.DataFrame(list(data_dict['labels'].items()), columns=['address', 'labels'])


    def build_dict(seq, key):
        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

    def load_protocols(file):
        with open(file) as f:
            data = json.load(f)
        protocols = data['protocols']
        protocol_by_name = build_dict(protocols, 'name')
        return protocol_by_name

    async def get_recent_transactions(contract_address, token_address, start_block = 25186796):
        c = Client(st.secrets['bscscan_apiKey'], api_kind='bsc')
        throttler = Throttler(rate_limit=4, period=1.0)
        try:
            transfers = await c.account.token_transfers(
                address = contract_address,
                contract_address = token_address,
                start_block=start_block,
                end_block=99999999
            )
            df_transfers = pd.DataFrame(transfers)
            for index, row in df_transfers.iterrows():
                print('pinging')
                temp = await c.proxy.tx_by_hash(row['hash'])
                time.sleep(0.15)
                row['from'] = temp['from']

                # df_transfers.loc[index, 'from'] = float(row['value']) / 10**18
            return df_transfers
        finally:
            await c.close()

    protocols = load_protocols('data/protocols.json')
    contract_address = protocols[contract_name]['address']

    # Start here
    # We can just read in transactions from here. 
    # df_transactions = pd.read_csv('output/transactions.csv')

    with open('/Users/asiah/Documents/dev/defi-terminal/output/hash_tx_from.txt', 'r') as f:
        json_data = f.read()

    # Load the JSON data into a dictionary
    data_dict = json.loads(json_data)

    # Create a DataFrame from the dictionary
    df_transactions = pd.DataFrame(data_dict)
    # # Takes in most recent transactions from a lp address
    # df_transactions = await get_recent_transactions(contract_address,token_address)
    # print(df_transactions.head())
    # # turns it into a dataframe
    # # df_transactions = pd.DataFrame(transactions)
    # df_transactions.to_csv('output/transactions.csv')

    ## End here
    # filters for those who's address are in a list of addresses
    df_labels = load_labels_to_df('output/classifications.json')
    df_filtered = df_transactions[df_transactions['from'].isin(df_labels['address']) | df_transactions['to'].isin(df_labels['address'])]
    # join the two df together to get the labels
    df_filtered = df_filtered.merge(df_labels, how='left', left_on='from', right_on='address')
    # df_filtered = df_filtered.merge(df_labels, how='left', left_on='to', right_on='address')
    # clean filtered dataframe
    df_filtered['datetime'] = pd.to_datetime(df_filtered['timeStamp'], unit='s')
    # return filtered dataframe
    # if to is wallet address, then value is negative
    df_final = df_filtered[['from', 'to', 'value', 'datetime', 'labels']].set_index('datetime')
    # df_final = df_final[['value']].astype(float)
    # df_final = df_final[['value']]/10**8
    # Look at those where labels is not null 
    df_final = df_final[df_final["labels"].str.len() != 0]
    # change the value to negative if from is the contract address
    df_final.loc[df_final['to'] == contract_address, 'value'] = df_final['value'] * -1 
    df_final = df_final[['labels','value','from','to']]
    # return df_final
    return df_final

df = asyncio.run(get_smartwallet_df('bnb_busd', "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"))
print(df.head())