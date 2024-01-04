import numpy as np
import pandas as pd
import json
from .optimization import max_sharp_ratio, portfolio_vol, portfolio_return

class Performance:

    def __init__(self, df_inp, df_portfolio, benchmark, risk_free_rate) -> None:
        super().__init__()
        self.risk_free_rate = risk_free_rate
        self.benchmark = benchmark
        self.returns = df_portfolio.drop(columns=benchmark).pct_change().dropna()
        self.annualized_returns = ((self.returns + 1).prod() ** (252 / self.returns.shape[0])) - 1
        self.dfp_index = df_portfolio.columns[:-1]
        self.df_inp = df_inp
        self.vola = []
        for i in range(len(df_inp)):
            ret = df_portfolio.iloc[:, [i]].pct_change()[1:]
            vol = np.sqrt(252 * ret.var())
            self.vola.append(vol[0])
        bench = df_portfolio[benchmark]
        self.benchm = bench[1:] * 100 / bench[1]
        self.opt_weight = None
    

    def individual_historical(self):

        indiv = pd.DataFrame(index=self.dfp_index)
        indiv['Company'] = self.df_inp.index.str.replace('.NS', "")
        indiv['Expected Return'] = self.annualized_returns * 100
        indiv['Volatility'] = self.vola
        
        indi = indiv.to_numpy().tolist()
        indexp = {'1': indi}
        
        return json.dumps(indexp)
    
    def optimization(self, risk_free_rate):

        self.opt_weight = max_sharp_ratio(self.annualized_returns, self.returns.cov(), risk_free_rate)

        inp3 = self.df_inp[["ltp", "buy_value", "now_value", "weightage"]].copy()

        inp3.index = inp3.index.str.replace('.NS', "")
        inp3['Opt_weight'] = self.opt_weight
        inp3['Opt_value'] = inp3['Opt_weight'] * np.sum(inp3['now_value'])
        inp3['Opt_quantity'] = (inp3['Opt_value'] / inp3['ltp']).astype(int)
        inp3 = inp3.drop(['ltp'], axis=1)
        # optimized weightage and quantity(Optimization)
        opt = inp3.reset_index().to_numpy()
        para = opt.tolist()
        optdict = {'1': para}

        return json.dumps(optdict)
    
    def original_portfolio_stats(self):

        weight1 = self.df_inp["weightage"].values
        
        percent_var1 = str(round(((portfolio_vol(weight1, self.returns.cov())) ** 2) * 100, 2)) + '%'
        percent_vols1 = str(round(portfolio_vol(weight1, self.returns.cov()) * 100, 2)) + '%'
        percent_ret1 = str(round(portfolio_return(weight1, self.annualized_returns) * 100, 2)) + '%'
        sharpe_ratio1 = str(round((portfolio_return(weight1, self.annualized_returns) - self.risk_free_rate) / portfolio_vol(weight1, self.returns.cov()),3))

        return percent_var1, percent_vols1, percent_ret1, sharpe_ratio1

    def optimized_portfolio_stats(self):
        weight2 = self.opt_weight

        percent_var2 = str(round(((portfolio_vol(weight2, self.returns.cov())) ** 2) * 100, 2)) + '%'
        percent_vols2 = str(round(portfolio_vol(weight2, self.returns.cov()) * 100, 2)) + '%'
        percent_ret2 = str(round(portfolio_return(weight2, self.annualized_returns) * 100, 2)) + '%'
        sharpe_ratio2 = str(round((portfolio_return(weight2, self.annualized_returns) - self.risk_free_rate) / portfolio_vol(weight2, self.returns.cov()),3))

        return percent_var2, percent_vols2, percent_ret2, sharpe_ratio2

    def performance_plot(self):

        w1 = np.array(self.df_inp["weightage"].values)
        w2 = np.array(self.opt_weight)

        # weighted returns
        weighted_returns1 = (w1 * self.returns)
        weighted_returns2 = (w2 * self.returns)

        # portfolio returns
        port_ret1 = weighted_returns1.sum(axis=1)
        port_ret2 = weighted_returns2.sum(axis=1)

        # cumulative portfolio returns
        cumulative_ret1 = (port_ret1 + 1).cumprod() * 100
        cumulative_ret2 = (port_ret2 + 1).cumprod() * 100

        # starting from 100(initial value)(can be converted as a user input)
        cumulative_ret1 = cumulative_ret1 * 100 / cumulative_ret1[0]
        cumulative_ret2 = cumulative_ret2 * 100 / cumulative_ret2[0]

        # cumret dataframe contains values to plot the portfolio performance .!.!
        cumret_tmp = pd.DataFrame(columns=['orig_value', 'opt_value', 'benchmark'])
        cumret_tmp['orig_value'] = cumulative_ret1
        cumret_tmp['opt_value'] = cumulative_ret2
        cumret_tmp['benchmark'] = self.benchm
        self.cumret = cumret_tmp.dropna()
        # --------------------------------------------------------------------------
        # Peformance Plot variables
        pltind = self.cumret.index.strftime("%Y-%m-%d").to_numpy().tolist()
        pltori = self.cumret['orig_value'].to_numpy().tolist()
        pltopt = self.cumret['opt_value'].to_numpy().tolist()
        pltbnc = self.cumret['benchmark'].to_numpy().tolist()
        pltdic = {'1': pltind, '2': pltori, '3': pltopt, '4': pltbnc}

        return json.dumps(pltdic)
    
    def yearly_returns(self, start_date):

        yearlyr = [self.cumret['orig_value'][0]]
        yearlyd = [start_date.year]
        for i in range(len(self.cumret)):
            if (int(self.cumret.index[i].year) > int(self.cumret.index[i - 1].year)):
                yearlyr.append(self.cumret['orig_value'][i])
                yearlyd.append(self.cumret.index[i].year)
        yearlyr.append(self.cumret['orig_value'][-1])

        yearlyr = pd.DataFrame(yearlyr)
        yr = yearlyr.pct_change()[1:] * 100
        yr["index"] = yearlyd
        yr['Yearly Return'] = yr[0]

        yr.drop([0], axis=1)
        yrl = yr['Yearly Return'].to_numpy().tolist()
        yri = yr['index'].to_numpy().tolist()
        yrdict = {'1': yri, '2':yrl}

        return json.dumps(yrdict)
    
    def monthly_returns(self):

        mnlyr = []
        mnlyr_m = []
        mnlyr_y = []

        for i in range(len(self.cumret)):
            if int(self.cumret.index[i].month) != int(self.cumret.index[i - 1].month):
                mnlyr.append(self.cumret['orig_value'][i])
                mnlyr_y.append(self.cumret.index[i].year)
                mnlyr_m.append(self.cumret.index[i].month)
        mnlyr.append(self.cumret['orig_value'][-1])

        mnr = pd.DataFrame(columns=['Year', 'Month', 'Value', 'Return'])
        mnr['Year'] = mnlyr_y
        mnr['Month'] = mnlyr_m
        mnr['Value'] = mnlyr[:-1]
        mnr['Return'] = mnr['Value'].pct_change().shift(-1) * 100

        mnrs = mnr[:-1]
        mnrs.drop(['Value'], axis=1)
        mnrs['ind'] = np.nan
        for i in range(len(mnrs)):
            mnrs['ind'].iloc[i] = str(mnrs['Year'].iloc[i]) + "-" + str(mnrs['Month'].iloc[i])
        mnrind = mnrs['ind'].to_numpy().tolist()
        mnrval = mnrs['Return'].to_numpy().tolist()
        mnlyret = {'1': mnrind, '2': mnrval}

        return json.dumps(mnlyret)