import numpy as np
import pandas as pd
import re
import datetime
from pandas_datareader import data as pdr
from scipy import stats, optimize
import json
# import yfinance as yf
from .tools import max_sharp_ratio, portfolio_vol, portfolio_return, ef_curve
from .features.allocation import Allocation
from .features.preprocess import PreProcess
from .features.performance import Performance

def analyze(data, ticker_symbols, buy_prices, quantities, risk_free_rate=0.03):

    preprocess = PreProcess(ticker_symbols, data, buy_prices, quantities)

    tickers = preprocess.tickers

    # define time range
    today = datetime.datetime.now().date()
    start_date = today - datetime.timedelta(weeks=260)
    end_date = today
    print(start_date)
    print(end_date)

    net_buy_value, net_now_value, total_pnl = preprocess.download_data(start_date, end_date)

    df_inp = preprocess.df_inp
    df_portfolio = preprocess.df_portfolio
    df_now = preprocess.df_now
    benchmark = preprocess.benchmark
    benchm = preprocess.benchm

    inpar = preprocess.df_inp.to_numpy() 
    paradict = json.dumps({'1': inpar.tolist()})

    # -----------------------------------------------------------------------------------
    # Portfolio Allocation

    allocation = Allocation('products/static_product/fundamentals.csv', preprocess.df_inp, tickers)

    company_pie_data = allocation.company_wise_allocation()
    cap_pie_data = allocation.cap_wise_allocation()
    sector_pie_data = allocation.sector_wise_allocation() 
    industry_pie_data = allocation.industry_wise_allocation() 

    # -----------------------------------------------------------------------------------------------
    # Individual Asset Stat

    weighted_pe, weighted_beta, pe = allocation.asset_fundamentals()

    #-----------------------------------------------
    #Performance

    performance = Performance(df_inp, df_portfolio, benchmark, risk_free_rate)
    returns = performance.returns
    indexp = performance.individual_historical()

    # --------------------------------------------------------------------------------------------
    # Calculating the optimized weights

    optdict = performance.optimization(risk_free_rate)

    # --------------------------------------------------------------------------------
    # Portfolio Statistics

    percent_var1 ,percent_vols1 ,percent_ret1, sharpe_ratio1 = performance.original_portfolio_stats()
    percent_var2 ,percent_vols2 ,percent_ret2, sharpe_ratio2 = performance.optimized_portfolio_stats()

    pltdict = performance.performance_plot()
    cumret = performance.cumret

    # --------------------------------------------------------------------------

    # Yearly and Monthly Returns Performance--------done-----------

    yrldict = performance.yearly_returns(start_date)
    mnlyret = performance.monthly_returns()


    # -------------------------------------------------------------------------------

    # Maximum Drawdown (PLOT)

    window = 252

    # ORIGINAL PORTFOLIO
    Roll_Max_c = cumret['orig_value'].rolling(window, min_periods=1).max()
    Daily_Drawdown_c = cumret['orig_value'] / Roll_Max_c - 1.0

    Max_Daily_Drawdown_c = Daily_Drawdown_c.rolling(
        window, min_periods=1).min()
    max_Drawdown_c = min(Daily_Drawdown_c)
    # to plot -->> Daily_Drawdown_c  && Max_Daily_Drawdown_c
    # print('Maximum Drawdown of Original Portfolio', max_Drawdown_c*100, '%')

    # OPTIMIZED PORTFOLIO
    Roll_Max_o = cumret['opt_value'].rolling(window, min_periods=1).max()
    Daily_Drawdown_o = cumret['opt_value'] / Roll_Max_o - 1.0

    Max_Daily_Drawdown_o = Daily_Drawdown_o.rolling(
        window, min_periods=1).min()
    max_Drawdown_o = min(Daily_Drawdown_o)
    # to plot -->> Daily_Drawdown_o  && Max_Daily_Drawdown_o
    # print('Maximum Drawdown of Optimized Portfolio', max_Drawdown_o*100, '%')

    # BENCHMARK
    Roll_Max_b = cumret['benchmark'].rolling(window, min_periods=1).max()
    Daily_Drawdown_b = cumret['benchmark'] / Roll_Max_b - 1.0

    Max_Daily_Drawdown_b = Daily_Drawdown_b.rolling(
        window, min_periods=1).min()
    max_Drawdown_b = min(Daily_Drawdown_b)
    # to plot -->> Daily_Drawdown_b  && Max_Daily_Drawdown_b
    # print('Maximum Drawdown of Benchmark', max_Drawdown_b*100, '%')

    # ----------------------------------------------------------------------------------
    # Efficient Frontier(PLOT)

    ef_plot = ef_curve(returns, risk_free_rate)
    # print(ef_plot)
    # ----------------------------------------------------------------------------------
    #Monte Carlo Forecast
    data_1 = cumret['orig_value']
    data_2 = cumret['opt_value']

    log_return1 = np.log(1 + data_1.pct_change())
    log_return2 = np.log(1 + data_2.pct_change())

    u1 = log_return1.mean()
    u2 = log_return2.mean()

    var1 = log_return1.var()
    var2 = log_return2.var()

    drift1 = u1 - (0.5 * var1)
    drift2 = u2 - (0.5 * var2)

    stdev1 = log_return1.std()
    stdev2 = log_return2.std()

    #---------------------------
    # can be taken as user input
    l = 500
    #how many trading sessions in future
    t_intervals = l
    #no. of omte carlo simulations
    iterations = 10000

    daily_returns1 = np.exp(drift1 + stdev1 * stats.norm.ppf(np.random.rand(t_intervals, iterations)))
    daily_returns2 = np.exp(drift2 + stdev2 * stats.norm.ppf(np.random.rand(t_intervals, iterations)))

    S0 = data_1.iloc[-1]
    S1 = data_2.iloc[-1]

    price_list1 = np.zeros_like(daily_returns1)
    price_list1[0] = S0
    price_list2 = np.zeros_like(daily_returns2)
    price_list2[0] = S1

    for t in range(1, t_intervals):
        price_list1[t] = price_list1[t - 1] * daily_returns1[t]
    
    high1 = max(price_list1[-1])
    median1 = np.median(price_list1[-1])
    low1 = min(price_list1[-1])
    print('For your Current Portfolio -->')
    print('100 Rs invested in {0} will be this much after 500 trading days from {1}'.format(start_date, end_date))
    print('The max prediction: ', high1)
    print('The median prediction: ', median1)
    print('The lowest prediction: ', low1)

    for t in range(1, t_intervals):
        price_list2[t] = price_list2[t - 1] * daily_returns2[t]

    high2 = max(price_list2[-1])
    median2 = np.median(price_list2[-1])
    low2 = min(price_list2[-1])
    print('For the Optimized Portfolio-->')
    print('100 Rs invested in {0} will be this much after 500 trading days from {1}'.format(start_date, end_date))
    print('The max prediction: ', high2)
    print('The median prediction: ', median2)
    print('The lowest prediction: ', low2)

    expected1 = pd.DataFrame(price_list1)
    expected2 = pd.DataFrame(price_list2)
    expected1['avg'] = expected1.mean(axis=1)
    expected2['avg'] = expected2.mean(axis=1)

    start = data_1.index[-1]
    times = pd.date_range(start, periods=l, freq='D')
    expected1.index = times
    expected2.index = times

    dfnew1 = pd.DataFrame(index = times)
    dfnew1['value'] = expected1['avg'].values
    dfnew2 = pd.DataFrame(index = times)
    dfnew2['value'] = expected2['avg'].values

    data_1.index = pd.to_datetime(data_1.index)
    data_2.index = pd.to_datetime(data_2.index)

    dfnew3 = dfnew2*data_1[-1]/dfnew2['value'][0]
    #print(dfnew1)
    #print(dfnew2)
    #print(dfnew3)
    dfnew = pd.DataFrame(index = dfnew1.index, columns=['a','b','c'])
    dfnew['a'] = dfnew1.values
    dfnew['b'] = dfnew2.values
    dfnew['c'] = dfnew3.values
    # print(dfnew)
    
    #comptime = np.concatenate((data_1.index, dfnew1.index))
    #mcd = pd.DataFrame(index= comptime)
    #mcd['a'] = 
    a = data_1 + dfnew1
    #mcd['b'] = data
    # print(len(a))
    # print(len(mcd))
    # print(mcd[1280:])
    
    comptime = dfnew.index.strftime("%Y-%m-%d").to_numpy().tolist()
    # comptime = comptime.tolist()
    montp1 = data_1.to_numpy().tolist()
    montp2 = data_2.to_numpy().tolist()
    monta = dfnew['a'].to_numpy().tolist()
    montb = dfnew['b'].to_numpy().tolist()
    montc = dfnew['c'].to_numpy().tolist()
    monte = {'D': comptime,'1': monta, '2': montb, '3': montc} #, '4': montp1, '5': montp2 }
    
    monte = json.dumps(monte)
    


    # -----------------------------------------------------------------------------------

    # all variables to be added in this dictionary
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'Current_Value': round(net_now_value, 0),
        'Invested_value': round(net_buy_value, 0),
        'Profit_loss': round(total_pnl, 0),
        'paradict': paradict,
        'company': company_pie_data,
        'cap': cap_pie_data,
        'sector': sector_pie_data,
        'industry': industry_pie_data,
        'optdict': optdict,
        'percent_ret1': percent_ret1,
        'percent_vols1': percent_vols1,
        'percent_var1': percent_var1,
        'percent_ret2': percent_ret2,
        'percent_vols2': percent_vols2,
        'percent_var2': percent_var2,
        'pe': pe,
        'indexp': indexp,
        'weighted_pe': weighted_pe,
        "weighted_beta": weighted_beta,
        'sharpe_ratio1': sharpe_ratio1,
        'sharpe_ratio2': sharpe_ratio2,
        'risk_free_rate': risk_free_rate * 100,
        'yrldict': yrldict,
        'mnlyret': mnlyret,
        'pltdict': pltdict,
        'monte': monte,
        'curmax': round(high1, 2),
        'curmed': round(median1, 2),
        'curlow': round(low1, 2),
        'optmax': round(high2, 2),
        'optmed': round(median2, 2),
        'optlow': round(low2, 2),
    }

    return context
