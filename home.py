import web3
import requests
import pandas as pd
import asyncio
import json
import time


import streamlit as st
import streamlit.components.v1 as components

import modules.goplus as goplus
import modules.smartwallet as smartwallet

st.set_page_config(
    page_title="Defi Terminal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.title('Pancake Swap BNB-USDT LP')
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

        components.html(
            """
            <!-- TradingView Widget BEGIN -->
            <div class="tradingview-widget-container">
            <div class="tradingview-widget-container__widget"></div>
            <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets</span></a> on TradingView</div>
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
            {
            "symbols": [
                [
                "BINANCE:BNBUSDT|1D"
                ]
            ],
            "chartOnly": false,
            "width": "100%",
            "height": "100%",
            "locale": "en",
            "colorTheme": "dark",
            "autosize": true,
            "showVolume": true,
            "showMA": false,
            "hideDateRanges": false,
            "hideMarketStatus": false,
            "hideSymbolLogo": false,
            "scalePosition": "right",
            "scaleMode": "Normal",
            "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
            "fontSize": "10",
            "noTimeScale": false,
            "valuesTracking": "1",
            "changeMode": "price-and-percent",
            "chartType": "area",
            "maLineColor": "#2962FF",
            "maLineWidth": 1,
            "maLength": 9,
            "lineWidth": 2,
            "lineType": 0
            }
            </script>
            </div>
            <!-- TradingView Widget END -->
            """
        )

        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader('Security')
            st.json(dapp_security)
            st.json(address_security)
        with right_column:
            st.subheader('Smart Wallet Flow')
            st.dataframe(smartwallet_df)

