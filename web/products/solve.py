# import libraries for function
import numpy as np
import pandas as pd
import re
import datetime
from pandas_datareader import data as pdr
from scipy import stats

# importing render
# from django.shortcuts import render
# from django.http import JsonResponse


def func1(data, ticker_symbol, buy_price, quantity):

    # getting ticker
    Ticks = []
    for i in range(len(ticker_symbol)):
        Ticks.append(ticker_symbol[i])
    tick = []

    for i in range(len(Ticks)):
        tick.append(Ticks[i].split('( ', 1)[1].split(' )')[0])
    inp = pd.DataFrame(index=tick)
    ticker_list = inp.index
    n = len(ticker_list)
    ticker = []
    for i in range(n):
        ticker.append(ticker_list[i]+str('.NS'))

    # define other user input
    inp["Quantity"] = quantity
    inp["Buy Price"] = buy_price
    # convert to float
    for i in range(len(inp)):
        inp['Quantity'][i] = float(inp['Quantity'][i])
        inp['Buy Price'][i] = float(inp['Buy Price'][i])
    print(inp)

    # define time range
    start_date = data['start_date']
    end_date = data['end_date']
    today = datetime.date.today()
    yester = today - datetime.timedelta(days=1)

    portfolio = pd.DataFrame()
    now = pd.DataFrame()
    # importing data from yahoo
    for i in range(n):
        portfolio[ticker[i]] = pdr.DataReader(ticker[i].strip(
            '\n'), data_source='yahoo', start=start_date, end=end_date)['Adj Close']
        now[ticker[i]] = pdr.DataReader(ticker[i].strip(
            '\n'), data_source='yahoo', start=yester, end=today)['Adj Close']

    # initialize benchmark
    if(data['benchmark'] == "NIFTY50"):
        benchmark = "^NSEI"
    elif(data['benchmark'] == "SENSEX"):
        benchmark = "^BSESN"
    # importing benchmark data
    bench = pdr.DataReader(benchmark, 'yahoo', start=start_date, end=end_date)[
        'Adj Close']
    benchm = bench*100/bench[0]

    # portfolio data statistics
    inp1 = inp
    inp1['ltp'] = np.nan
    for i in range(n):
        inp['ltp'].iloc[i] = now[ticker[i]].iloc[-1]
    inp1['buy_value'] = inp1['Quantity']*inp1['Buy Price']
    inp1['now_value'] = inp1['Quantity']*inp1['ltp']
    inp1['pnl'] = inp1['now_value']-inp1['buy_value']
    total_pnl = np.sum(inp1['pnl'])
    net_buy_value = np.sum(inp1['buy_value'])
    net_now_value = np.sum(inp1['now_value'])
    inp1['Weightage'] = inp1['now_value']/net_now_value

    print(inp1.to_numpy())
    print('Current Value : ', net_now_value)
    print('Invested Value : ', net_buy_value)
    print('Profit / Loss : ', total_pnl)
    # -----------------------------------------------------------------------------------

    #Sectorwise/Industrywise Allocation
    listed = pd.read_csv('products/static_product/fundamentals.csv', index_col='Ticker')
    inp2 = inp1.copy()
    list_con = pd.concat([inp2,listed], axis=1, sort = False)
    #dat1 is the dataframe with Sector Allocation by Value
    dat1 = list_con.groupby(['Sector'])['now_value'].agg('sum')
    dat1 = dat1.replace(0, np.nan)
    dat1.dropna(inplace=True)
    print(dat1)
    # dat2 is the dataframe with Industry Allocation by Value
    dat2 = list_con.groupby(['Industry'])['now_value'].agg('sum')
    dat2 = dat2.replace(0, np.nan)
    dat2.dropna(inplace=True)
    print(dat2)

    # Weighted PE Ratio
    list_con['buy_value'] = list_con['buy_value'].dropna(inplace=True)
    list_pe = list_con[['Price to Earnings Ratio (TTM)', 'now_value']]
    list_pe = list_pe.iloc[:len(inp2)]
    weighted_pe = np.sum(
        list_pe['Price to Earnings Ratio (TTM)']*list_pe['now_value']/net_now_value)
    print(list_pe)
    print("Weighted PE :", weighted_pe)
    # --------------------------------------------------------------------------------------------

    # Calculating the optimized weights
    log_ret = np.log(portfolio/portfolio.shift(1))

    np.random.seed(42)
    num_ports = 6000
    all_weights = np.zeros((num_ports, len(portfolio.columns)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)

    for x in range(num_ports):
        # Weights
        weights = np.array(np.random.random(n))
        weights = weights/np.sum(weights)

        # Save weights
        all_weights[x, :] = weights

        # Expected return
        ret_arr[x] = np.sum((log_ret.mean() * weights * 252))

        # Expected volatility
        vol_arr[x] = np.sqrt(
            np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))

        # Sharpe Ratio
        sharpe_arr[x] = ret_arr[x]/vol_arr[x]

    print('Max Sharpe ratio= {}'.format(sharpe_arr.max()))
    l = sharpe_arr.argmax()

    opt_weight = all_weights[l]

    max_sr_ret = ret_arr[sharpe_arr.argmax()]
    max_sr_vol = vol_arr[sharpe_arr.argmax()]

    inp3 = inp1.copy()
    inp3['Opt_weight'] = opt_weight
    inp3['Opt_value'] = inp3['Opt_weight']*np.sum(inp3['now_value'])
    inp3['Opt_quantity'] = (inp3['Opt_value']/inp3['ltp'])
    inp3['Opt_quantity'] = inp3['Opt_quantity'].astype(int)

    # optimized weightage and quantity(Optimization)
    print(inp3)
    # --------------------------------------------------------------------------------

    # individual asset plot (portfolio1)
    portfolio1 = portfolio*100/portfolio.iloc[0]

    returns = portfolio.pct_change()
    returns = returns.iloc[1:]

    cov_matrix_annual = returns.cov() * 252

    # Original & Optimal Weights
    weight1 = inp1["Weightage"].values
    weight2 = opt_weight
    print(weight1)
    # Portfolio Variance
    port_variance1 = np.dot(weight1.T, np.dot(cov_matrix_annual, weight1))
    port_variance2 = np.dot(weight2.T, np.dot(cov_matrix_annual, weight2))
    # Portfolio Volatility
    port_volatility1 = np.sqrt(port_variance1)
    port_volatility2 = np.sqrt(port_variance2)
    # Annual Return (CAGR)(both)
    portfolioSimpleAnnualReturn1 = np.sum(returns.mean()*weight1) * 252
    portfolioSimpleAnnualReturn2 = np.sum(returns.mean()*weight2) * 252

    # Historical Data Statistics
    percent_var1 = str(round(port_variance1, 2) * 100) + '%'
    percent_vols1 = str(round(port_volatility1, 2) * 100) + '%'
    percent_ret1 = str(round(portfolioSimpleAnnualReturn1, 2)*100)+'%'
    percent_var2 = str(round(port_variance2, 2) * 100) + '%'
    percent_vols2 = str(round(port_volatility2, 2) * 100) + '%'
    percent_ret2 = str(round(portfolioSimpleAnnualReturn2, 2)*100)+'%'
    print('Original Statistics ->')
    print("Expected annual return : " + percent_ret1)
    print('Annual volatility/standard deviation/risk : '+percent_vols1)
    print('Annual variance : '+percent_var1)
    print('Optimized Statistics ->')
    print("Expected annual return : " + percent_ret2)
    print('Annual volatility/standard deviation/risk : '+percent_vols2)
    print('Annual variance : '+percent_var2)

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
    cumulative_ret1 = (port_ret1 + 1).cumprod()*100
    cumulative_ret2 = (port_ret2 + 1).cumprod()*100

    # starting from 100(initial value)(can be converted as a user input)
    cumulative_ret1 = cumulative_ret1*100/cumulative_ret1[0]
    cumulative_ret2 = cumulative_ret2*100/cumulative_ret2[0]

    # cumret dataframe contains values to plot the portfolio performance .!.!
    cumret = pd.DataFrame(columns=['orig_value', 'opt_value', 'benchmark'])
    cumret['orig_value'] = cumulative_ret1
    cumret['opt_value'] = cumulative_ret2
    cumret['benchmark'] = benchm
    print(cumret)
    # --------------------------------------------------------------------------

    # Calculating the beta of the portfolio

    # ----------------------------------------------------------------

    # Yearly Return Performance

    yearlyr = [cumret['orig_value'][0]]
    yearlyd = [start_date.year]
    for i in range(len(cumret)):
        if(int(cumret.index[i].year) > int(cumret.index[i-1].year)):
            yearlyr.append(cumret['orig_value'][i])
            yearlyd.append(cumret.index[i].year)
    yearlyr.append(cumret['orig_value'][-1])

    yearlyr = pd.DataFrame(yearlyr)

    yr = yearlyr.pct_change()[1:]*100
    yr.index = yearlyd
    yr['Yearly Return'] = yr[0]

    yr.drop([0], axis=1)
    print("Historical Yearly Returns of the Portfolio(BAR)")
    print(yr['Yearly Return'])

    # -------------------------------------------------------------------------------

    # Monthly Return Performance

    mnlyr = []
    mnlyr_m = []
    mnlyr_y = []

    for i in range(len(cumret)):
        if(int(cumret.index[i].month) != int(cumret.index[i-1].month)):
            mnlyr.append(cumret['orig_value'][i])
            mnlyr_y.append(cumret.index[i].year)
            mnlyr_m.append(cumret.index[i].month)
    mnlyr.append(cumret['orig_value'][-1])

    mnr = pd.DataFrame(columns=['Year', 'Month', 'Value', 'Return'])
    mnr['Year'] = mnlyr_y
    mnr['Month'] = mnlyr_m
    mnr['Value'] = mnlyr[:-1]
    mnr['Return'] = mnr['Value'].pct_change().shift(-1)*100

    mnrs = mnr[:-1]
    mnrs.drop(['Value'], axis=1)
    print("Historical Monthly Returns of the Portfolio(BAR)")
    print(mnrs)

    # -------------------------------------------------------------------------------

    # Maximum Drawdown (PLOT)

    window = 252

    # ORIGINAL PORTFOLIO
    Roll_Max_c = cumret['orig_value'].rolling(window, min_periods=1).max()
    Daily_Drawdown_c = cumret['orig_value']/Roll_Max_c - 1.0

    Max_Daily_Drawdown_c = Daily_Drawdown_c.rolling(
        window, min_periods=1).min()
    max_Drawdown_c = min(Daily_Drawdown_c)
    # to plot -->> Daily_Drawdown_c  && Max_Daily_Drawdown_c
    print('Maximum Drawdown of Original Portfolio', max_Drawdown_c*100, '%')

    # OPTIMIZED PORTFOLIO
    Roll_Max_o = cumret['opt_value'].rolling(window, min_periods=1).max()
    Daily_Drawdown_o = cumret['opt_value']/Roll_Max_o - 1.0

    Max_Daily_Drawdown_o = Daily_Drawdown_o.rolling(
        window, min_periods=1).min()
    max_Drawdown_o = min(Daily_Drawdown_o)
    # to plot -->> Daily_Drawdown_o  && Max_Daily_Drawdown_o
    print('Maximum Drawdown of Optimized Portfolio', max_Drawdown_o*100, '%')

    # BENCHMARK
    Roll_Max_b = cumret['benchmark'].rolling(window, min_periods=1).max()
    Daily_Drawdown_b = cumret['benchmark']/Roll_Max_b - 1.0

    Max_Daily_Drawdown_b = Daily_Drawdown_b.rolling(
        window, min_periods=1).min()
    max_Drawdown_b = min(Daily_Drawdown_b)
    # to plot -->> Daily_Drawdown_b  && Max_Daily_Drawdown_b
    print('Maximum Drawdown of Benchmark', max_Drawdown_b*100, '%')

    # ----------------------------------------------------------------------------------

    # Individual Asset Statistics

    # ----------------------------------------------------------------------------------

    # Efficient Frontier(PLOT)

    # ----------------------------------------------------------------------------------

    # all variables to be added in this dictionary
    context = {
        'Current_Value': round(net_now_value, 0),
        'Invested_value': round(net_buy_value, 0),
        'Profit_loss': round(total_pnl, 0),
        'inp1': inp1.to_html(),
        'inpp1c': inp1.columns,
        'inpp1i': inp1.index,
        'inpp1r':inp1.to_numpy(),

    }

    return context
