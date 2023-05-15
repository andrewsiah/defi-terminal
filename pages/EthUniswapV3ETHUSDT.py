import web3
import requests
import pandas as pd
import asyncio
import json
import time

from aioetherscan import Client
from asyncio_throttle import Throttler
import streamlit as st
import streamlit.components.v1 as components


import modules.goplus as goplus
import modules.smartwallet as smartwallet


# embed streamlit docs in a streamlit app
# components.iframe(
#     "https://pancakeswap.finance/add/BNB/0x55d398326f99059ff775485246999027b3197955",
#      height=600)
# Security

st.title('Eth Uniswap V3 ETH-USDT LP')
dapp_security, address_security = goplus.get_security('contracts/chains/binance-smart-chain/bep20_pools.json', 'add_bnb_usdt')

# Smart Wallet
smartwallet_df = asyncio.run(smartwallet.get_smartwallet_df('bnb_busd', '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'))
outflow = 1000
inflow = 10000

placeholder = st.empty()
while True:
    with placeholder.container():
        l,m,r = st.columns(3)
        with l:
            st.subheader('Position')
            st.write('2.23000')
        with m:
            st.subheader('Position ($)')
            st.write('$423.24')
        with r:
            st.subheader('Inflow/Outflow of Pool (24H)')
            st.write('-122/3124422')


        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader('Security')
            st.json(dapp_security)
            st.json(address_security)
        with right_column:
            st.subheader('Smart Wallet Flow')
            st.dataframe(smartwallet_df)

s