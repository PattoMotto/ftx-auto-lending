import pandas as pd
import numpy as np
import time
import ccxt
from exchangeClient import ExchangeClient
import os

class LendingStakingBot:
    
    def loadLending(self):
        lendingDf = pd.read_csv('lending.csv')
        lendingDf['reserved'] = lendingDf['reserved'].astype(np.float64)
        self.lendings = lendingDf.to_dict('records')
    
    def loop(self):
        self.loadLending()
        for lendingData in self.lendings:
            self.autoLending(lendingData)
            time.sleep(1)

    def autoLending(self, lendingData):
        exchangeClient = self.getExchangeClient(lendingData)
        currency = lendingData['currency']
        reserved = lendingData['reserved']
        balance = exchangeClient.getBalance(currency)
        if balance == 0:
            return
        size = balance - reserved if reserved < balance else 0
        exchangeClient.lendAsset(coin=currency, size=size)
        print(f'Subaccount: {lendingData["subaccount"]} Lend: {size:.8f} {currency}')

    def getExchangeClient(self, lendingData):
        # Exchange Detail
        exchange = ccxt.ftx({ 'apiKey': lendingData['api_key'] ,'secret': lendingData['secret'] ,'enableRateLimit': True })
        subaccount = lendingData['subaccount']
        if len(subaccount) > 0:
            exchange.headers = { 'FTX-SUBACCOUNT': lendingData['subaccount'] }
        # exchange.verbose = True
        return ExchangeClient(exchange)

    def setFirstRowAsColumn(self, dataFrame):
        dataFrame.columns = dataFrame.iloc[0]
        dataFrame = dataFrame[1:]
        return dataFrame
