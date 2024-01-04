import numpy as np
import pandas as pd
import yfinance as yf
import datetime

class PreProcess:

    def __init__(self, ticker_symbols, data, buy_prices, quantity) -> None:
        super().__init__()
        self.ticker_symbols = ticker_symbols
        self.buy_prices = buy_prices
        self.quantity = quantity

        self.tickers = [i.split('( ', 1)[1].split(' )')[0] + ".NS" for i in ticker_symbols]
        
        # df_inp (input dataframe)
        self.df_inp = pd.DataFrame(index=self.tickers)
        self.df_inp.index.name = "Ticker"
        self.df_inp['Company'] = self.df_inp.index.str.replace('.NS', "")
        self.df_inp["quantity"] = np.array(quantity).astype(float)
        self.df_inp["buy_price"] = np.array(buy_prices).astype(float)

        self.benchmark = ""
        if data['benchmark'] == "NIFTY50":
            self.benchmark = "^NSEI"
        elif data['benchmark'] == "SENSEX":
            self.benchmark = "^BSESN"

        self.tickers.append(self.benchmark)

        self.df_portfolio = pd.DataFrame()
        self.df_now = pd.DataFrame()

    

    def download_data(self, start_date, end_date):

        yf_data = yf.download(
            tickers=self.tickers,
            start=start_date,
            end=end_date + datetime.timedelta(days=1),
            interval='1d',
            group_by='ticker'
        )
        yf_data_current = yf.download(
            tickers=self.tickers,
            start=datetime.datetime.now().date() - datetime.timedelta(days=15),
            end=datetime.datetime.now().date() + datetime.timedelta(days=1),
            interval='1d',
            group_by='ticker'
        )

        for i in self.tickers:
            self.df_portfolio[i] = yf_data[i]["Adj Close"]
            self.df_now[i] = yf_data_current[i]["Adj Close"]

        # importing benchmark data
        bench = self.df_portfolio[self.benchmark]
        self.benchm = bench[1:] * 100 / bench[1]
        self.df_inp['ltp'] = np.nan

        for i in self.tickers:
            self.df_inp['ltp'].loc[i] = round(self.df_now[i].iloc[-1], 2)

        self.df_inp['buy_value'] = self.df_inp['quantity'] * self.df_inp['buy_price']
        self.df_inp['now_value'] = self.df_inp['quantity'] * self.df_inp['ltp']
        self.df_inp['pnl'] = self.df_inp['now_value'] - self.df_inp['buy_value']
        self.df_inp['perc_gain'] = self.df_inp['pnl'] * 100 / self.df_inp['buy_value']
        total_pnl = np.sum(self.df_inp['pnl'])
        net_buy_value = np.sum(self.df_inp['buy_value'])
        net_now_value = np.sum(self.df_inp['now_value'])
        self.df_inp['weightage'] = self.df_inp['now_value'] / net_now_value
        return net_buy_value, net_now_value, total_pnl
