import numpy as np
import pandas as pd
import re
import datetime
from pandas_datareader import data as pdr
from scipy import stats, optimize
import json
import yfinance as yf
from .tools import max_sharp_ratio, portfolio_vol, portfolio_return, ef_curve

data_ = {
    'Portfolio_type': 'Tickers',
    'benchmark': 'NIFTY50',
    'start_date': datetime.datetime(2015, 1, 1),
    'end_date': datetime.datetime(2020, 7, 1),
    'number_of_portfolio': 2,
}

ticker_symbol_ = ['Reliance Industries Limited ( RELIANCE )', 'Hindustan Unilever Limited ( HINDUNILVR )']
buy_prices_ = ['900', '900']
quantities_ = ['10', '10']


def func1(data, ticker_symbols, buy_prices, quantities, risk_free_rate=0.03):
    print("$$$$$$$$$$$$$$$$$$")
    print(data)
    print(ticker_symbols)
    print(buy_prices)
    print(quantities)

    tickers = [i.split('( ', 1)[1].split(' )')[0] + ".NS" for i in ticker_symbols]
    print("Tickers: ", tickers)

    df_inp = pd.DataFrame(index=tickers)
    df_inp.index.name = "Ticker"

    # define other user input
    df_inp['Company'] = df_inp.index.str.replace('.NS', "")
    df_inp["quantity"] = np.array(quantities).astype(float)
    df_inp["buy_price"] = np.array(buy_prices).astype(float)
    print(df_inp)

    # define time range
    today = datetime.datetime.now().date()
    # start_date = data['start_date']
    # end_date = data['end_date']
    start_date = datetime.datetime(2015, 1, 1)  # today - datetime.timedelta(weeks=250 )
    end_date = today
    yesterday = today - datetime.timedelta(days=3)
    print("Yesterday:", yesterday)
    df_portfolio = pd.DataFrame()
    df_now = pd.DataFrame()

    # initialize benchmark
    benchmark = ""
    if data['benchmark'] == "NIFTY50":
        benchmark = "^NSEI"
    elif data['benchmark'] == "SENSEX":
        benchmark = "^BSESN"

    tickers.append(benchmark)

    # importing data from yahoo
    print(start_date)
    print(end_date)
    yf_data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date + datetime.timedelta(days=1),
        interval='1d',
        group_by='ticker'
    )

    yf_data_current = yf.download(
        tickers=tickers,
        start=datetime.datetime.now().date() - datetime.timedelta(days=15),
        end=datetime.datetime.now().date() + datetime.timedelta(days=1),
        interval='1d',
        group_by='ticker'
    )

    for i in tickers:
        df_portfolio[i] = yf_data[i]["Adj Close"]
        df_now[i] = yf_data_current[i]["Adj Close"]

    # importing benchmark data
    bench = df_portfolio[benchmark]
    benchm = bench[1:] * 100 / bench[1]
    # print(bench)
    df_inp['ltp'] = np.nan

    for i in tickers:
        df_inp['ltp'].loc[i] = round(df_now[i].iloc[-1], 2)

    df_inp['buy_value'] = df_inp['quantity'] * df_inp['buy_price']
    df_inp['now_value'] = df_inp['quantity'] * df_inp['ltp']
    df_inp['pnl'] = df_inp['now_value'] - df_inp['buy_value']
    df_inp['perc_gain'] = df_inp['pnl'] * 100 / df_inp['buy_value']
    total_pnl = np.sum(df_inp['pnl'])
    net_buy_value = np.sum(df_inp['buy_value'])
    net_now_value = np.sum(df_inp['now_value'])
    df_inp['weightage'] = df_inp['now_value'] / net_now_value
    print(df_inp)
    print("printed")

    inpar = df_inp.to_numpy()
    para = inpar.tolist()
    pardict = {'1': para}
    paradict = json.dumps(pardict)
    # print('Current Value : ', net_now_value)
    # print('Invested Value : ', net_buy_value)
    # print('Profit / Loss : ', total_pnl)
    # -----------------------------------------------------------------------------------

    # Portfolio Allocation

    df_listed = pd.read_csv('products/static_product/fundamentals.csv', index_col='Ticker')
    df_listed.index = df_listed.index.astype(str) + '.NS'
    df_inp = df_inp.join(df_listed[df_listed.index.isin(tickers)])

    group_company = df_inp.groupby(['Ticker']).agg('sum')['now_value']
    company_pie_values = group_company.to_list()
    company_pie_names = group_company.index.tolist()
    company_pie_data = json.dumps({'1': company_pie_values, '2': company_pie_names})

    group_cap = df_inp.groupby(['Cap']).agg('sum')['now_value']
    cap_pie_values = group_cap.to_list()
    cap_pie_names = group_cap.index.tolist()
    cap_pie_data = json.dumps({'1': cap_pie_values, '2': cap_pie_names})

    group_sector = df_inp.groupby(['Sector']).agg('sum')['now_value']
    sector_pie_values = group_sector.tolist()
    sector_pie_names = group_sector.index.tolist()
    sector_pie_data = json.dumps({'1': sector_pie_values, '2': sector_pie_names})

    group_industry = df_inp.groupby(['Industry']).agg('sum')['now_value']
    industry_pie_values = group_industry.tolist()
    industry_pie_names = group_industry.index.tolist()
    industry_pie_data = json.dumps({'1': industry_pie_values, '2': industry_pie_names})

    # -----------------------------------------------------------------------------------------------
    # Individual Asset Stat
    weighted_pe = np.sum(df_inp["Price to Earnings Ratio (TTM)"] * df_inp['now_value'] / net_now_value)
    weighted_beta = np.sum(df_inp["1-Year Beta"] * df_inp['now_value'] / net_now_value)
    list_pe = df_inp[['Cap', 'Industry', '1-Year Beta', 'Price to Earnings Ratio (TTM)', 'Basic EPS (TTM)']].copy()
    list_pe.index = list_pe.index.str.replace('.NS', "")
    pelist = list_pe.reset_index().to_numpy().tolist()
    pe = {'1': pelist}
    pe = json.dumps(pe)
    # print("Weighted PE :", weighted_pe)

    #-----------------------------------------------
    returns = df_portfolio.drop(columns=benchmark).pct_change().dropna()
    annualized_returns = ((returns + 1).prod() ** (252 / returns.shape[0])) - 1
    #-----------------------------------------------
    
    window_size = 100
    vola = []
    for i in range(len(df_inp)):
        ret = df_portfolio.iloc[:, [i]].pct_change()[1:]
        vol = np.sqrt(252 * ret.var())
        vola.append(vol[0])

    # Individual Expected Return / Volatility
    indiv = pd.DataFrame(index=df_portfolio.columns[:-1])
    indiv['Company'] = df_inp.index.str.replace('.NS', "")
    indiv['Expected Return'] = annualized_returns * 100
    indiv['Volatility'] = vola
    
    indi = indiv.to_numpy().tolist()
    indexp = {'1': indi}
    indexp = json.dumps(indexp)

    # --------------------------------------------------------------------------------------------

    # Calculating the optimized weights

    # print(annualized_returns)
    opt_weight = max_sharp_ratio(annualized_returns, returns.cov(), risk_free_rate)

    # max_sr_ret = portfolio_return(opt_weight, annualized_returns)
    # max_sr_vol = portfolio_vol(opt_weight, returns.cov())

    inp3 = df_inp[["ltp", "buy_value", "now_value", "weightage"]].copy()

    inp3.index = inp3.index.str.replace('.NS', "")
    inp3['Opt_weight'] = opt_weight
    inp3['Opt_value'] = inp3['Opt_weight'] * np.sum(inp3['now_value'])
    inp3['Opt_quantity'] = (inp3['Opt_value'] / inp3['ltp']).astype(int)
    inp3 = inp3.drop(['ltp'], axis=1)
    # optimized weightage and quantity(Optimization)
    opt = inp3.reset_index().to_numpy()
    para = opt.tolist()
    optdict = {'1': para}
    optdict = json.dumps(optdict)
    # print(inp3)
    # --------------------------------------------------------------------------------

    # individual asset plot (portfolio1)
    # portfolio1 = df_portfolio * 100 / df_portfolio.iloc[0]

    returns = df_portfolio.pct_change().drop(columns=benchmark)
    returns = returns.iloc[1:]

    cov_matrix_annual = returns.cov() * 252

    # Original & Optimal Weights
    weight1 = df_inp["weightage"].values
    weight2 = opt_weight
    # print(weight1)
    # Portfolio Variance
    # port_variance1 = np.dot(weight1.T, np.dot(cov_matrix_annual, weight1))
    # port_variance2 = np.dot(weight2.T, np.dot(cov_matrix_annual, weight2))
    # Portfolio Volatility
    # port_volatility1 = np.sqrt(port_variance1)
    # port_volatility2 = np.sqrt(port_variance2)
    # Annual Return (CAGR)(both)
    # portfolioSimpleAnnualReturn1 = np.sum(returns.mean() * weight1) * 252
    # portfolioSimpleAnnualReturn2 = np.sum(returns.mean() * weight2) * 252

    # Historical Data Statistics
    percent_var1 = str(round(((portfolio_vol(weight1, returns.cov())) ** 2) * 100, 2)) + '%'
    percent_vols1 = str(round(portfolio_vol(weight1, returns.cov()) * 100, 2)) + '%'
    percent_ret1 = str(round(portfolio_return(weight1, annualized_returns) * 100, 2)) + '%'
    percent_var2 = str(round(((portfolio_vol(weight2, returns.cov())) ** 2) * 100, 2)) + '%'
    percent_vols2 = str(round(portfolio_vol(weight2, returns.cov()) * 100, 2)) + '%'
    percent_ret2 = str(round(portfolio_return(weight2, annualized_returns) * 100, 2)) + '%'

    # net_portfolio_return1 = str(round(portfolio_return(weight1, annualized_returns), 3) * 100) + '%'
    # net_portfolio_return2 = str(round(portfolio_return(weight2, annualized_returns), 3) * 100) + '%'
    # net_portfolio_volatility1 = str(round(portfolio_vol(weight1, returns.cov()), 3))
    # net_portfolio_volatility2 = str(round(portfolio_vol(weight2, returns.cov()), 3))

    sharpe_ratio1 = str(round(
        (portfolio_return(weight1, annualized_returns) - risk_free_rate) / portfolio_vol(weight1, returns.cov()),
        3))

    sharpe_ratio2 = str(round(
        (portfolio_return(weight2, annualized_returns) - risk_free_rate) / portfolio_vol(weight2, returns.cov()),
        3))

    # cagr_1 = ""
    # cagr_2 = ""
    # print('Original Statistics ->')
    # print("Expected annual return : " + percent_ret1)
    # print('Annual volatility/standard deviation/risk : '+percent_vols1)
    # print('Annual variance : '+percent_var1)
    # print('Optimized Statistics ->')
    # print("Expected annual return : " + percent_ret2)
    # print('Annual volatility/standard deviation/risk : '+percent_vols2)
    # print('Annual variance : '+percent_var2)

    # Original and Optimized weights
    w1 = np.array(weight1)
    w2 = np.array(weight2)

    # weighted returns
    weighted_returns1 = (w1 * returns)
    weighted_returns2 = (w2 * returns)

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
    cumret = pd.DataFrame(columns=['orig_value', 'opt_value', 'benchmark'])
    cumret['orig_value'] = cumulative_ret1
    cumret['opt_value'] = cumulative_ret2
    cumret['benchmark'] = benchm
    # print(cumret)
    cumret = cumret.dropna()
    # --------------------------------------------------------------------------
    # Peformance Plot variables
    pltind = cumret.index.strftime("%Y-%m-%d").to_numpy().tolist()
    pltori = cumret['orig_value'].to_numpy().tolist()
    pltopt = cumret['opt_value'].to_numpy().tolist()
    pltbnc = cumret['benchmark'].to_numpy().tolist()
    pltdic = {'1': pltind, '2': pltori, '3': pltopt, '4': pltbnc}
    pltdict = json.dumps(pltdic)
    # print(pltdict)

    # --------------------------------------------------------------------------

    # Yearly Return Performance--------done-----------

    yearlyr = [cumret['orig_value'][0]]
    yearlyd = [start_date.year]
    for i in range(len(cumret)):
        if (int(cumret.index[i].year) > int(cumret.index[i - 1].year)):
            yearlyr.append(cumret['orig_value'][i])
            yearlyd.append(cumret.index[i].year)
    yearlyr.append(cumret['orig_value'][-1])

    yearlyr = pd.DataFrame(yearlyr)

    yr = yearlyr.pct_change()[1:] * 100
    yr.index = yearlyd
    yr['Yearly Return'] = yr[0]

    yr.drop([0], axis=1)
    # print("Historical Yearly Returns of the Portfolio(BAR)")
    yrl = yr['Yearly Return'].to_numpy().tolist()
    yrdict = {'1': yrl}
    yrldict = json.dumps(yrdict)
    # print(yrldict)

    # -------------------------------------------------------------------------------

    # Monthly Return Performance---------done-----------------

    mnlyr = []
    mnlyr_m = []
    mnlyr_y = []

    for i in range(len(cumret)):
        if int(cumret.index[i].month) != int(cumret.index[i - 1].month):
            mnlyr.append(cumret['orig_value'][i])
            mnlyr_y.append(cumret.index[i].year)
            mnlyr_m.append(cumret.index[i].month)
    mnlyr.append(cumret['orig_value'][-1])

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
    mnlyret = json.dumps(mnlyret)
    # print(mnrs)
    # yrl = yr['Yearly Return'].to_numpy().tolist()
    # yrdict = {'1': yrl}
    # yrldict = json.dumps(yrdict)
    # print(yrldict)

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

    # Individual Asset Statistics

    # ----------------------------------------------------------------------------------

    # Efficient Frontier(PLOT)

    ef_plot = ef_curve(returns, risk_free_rate)
    #print(ef_plot)
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
    iterations = 10

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
    print(dfnew)
    
    comptime = np.concatenate((data_1.index, dfnew1.index))
    mcd = pd.DataFrame(index= comptime)
    #mcd['a'] = 
    a = data_1 + dfnew1
    #mcd['b'] = data
    print(len(a))
    print(len(mcd))
    print(mcd[1280:])

    comptime = comptime.tolist()
    montp1 = data_1.to_numpy().tolist()
    montp2 = data_2.to_numpy().tolist()
    monta = dfnew['a'].to_numpy().tolist()
    montb = dfnew['b'].to_numpy().tolist()
    montc = dfnew['c'].to_numpy().tolist()
    monte = {'D': comptime,'1': monta, '2': montb, '3': montc, '4': montp1, '5': montp2 }
    monte = json.dumps(monte)
    

    # -----------------------------------------------------------------------------------

    # all variables to be added in this dictionary
    context = {
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
    }

    return context
