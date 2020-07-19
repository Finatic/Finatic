from django.shortcuts import render
from .forms import port_opti
from django.http import JsonResponse

# import libraries for function
import numpy as np
import pandas as pd
import re
import datetime
from pandas_datareader import data as pdr


# Create your views here.

def portfolio(request):
    message = []
    if request.method == 'POST':
        form = port_opti(request.POST)

        if form.is_valid():
            portfolio_type = form.cleaned_data['Portfolio_type']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            nop = form.cleaned_data['number_of_portfolio']
            benchmark = form.cleaned_data['benchmark']
            ticker_symbol = []
            quantity = []
            buy_price = []
            for i in range(1, nop+1):
                a = form.cleaned_data['ticker_symbol_'+str(i)]
                b = form.data['quantity_'+str(i)]
                c = form.data['buy_price_'+str(i)]
                ticker_symbol.append(a)
                quantity.append(b)
                buy_price.append(c)

            print(ticker_symbol)
            print(buy_price)
            print(quantity)
            data = form.cleaned_data
            solve(request, data, ticker_symbol, buy_price, quantity)
            # inp1 = solve(request, data, ticker_symbol, buy_price, quantity)
            return JsonResponse(data)

        else:
            error = form.errors.as_data()
            message.append(error)
            return render(request, 'home.html', {'message': message})
    else:
        form = port_opti
        data = []
        for i in range(1, 11):
            data.append(i)
        return render(request, 'product/portfolio.html', {'form': form, "number": data})


def solve(request, data, ticker_symbol, buy_price, quantity):
    Ticks = []
    for i in range(len(ticker_symbol)):
        Ticks.append(ticker_symbol[i])
    tick = []
    for i in range(len(Ticks)):
        tick.append(Ticks[i].split('( ', 1)[1].split(' )')[0])
    inp = pd.DataFrame(index=tick)
    inp["Quantity"] = quantity
    inp["Buy Price"] = buy_price
    print(inp)
    start_date = data['start_date']
    end_date = data['end_date']
    today = datetime.date.today()
    yester = today - datetime.timedelta(days=1)
    for i in range(len(inp)):
        inp['Quantity'][i] = float(inp['Quantity'][i])
        inp['Buy Price'][i] = float(inp['Buy Price'][i])
    ticker_list = inp.index
    n = len(ticker_list)
    ticker = []
    for i in range(n):
        ticker.append(ticker_list[i]+str('.NS'))
    portfolio = pd.DataFrame()
    now = pd.DataFrame()
    # importing data from yahoo
    for i in range(n):
        portfolio[ticker[i]] = pdr.DataReader(ticker[i].strip(
            '\n'), data_source='yahoo', start=start_date, end=end_date)['Adj Close']
        now[ticker[i]] = pdr.DataReader(ticker[i].strip(
            '\n'), data_source='yahoo', start=yester, end=today)['Adj Close']

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

    print(inp1)
    print('Current Value : ', net_now_value)
    print('Invested Value : ', net_buy_value)
    print('Profit / Loss : ', total_pnl)

    #Calculating the optimized weights
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
        all_weights[x,:] = weights
        
        # Expected return
        ret_arr[x] = np.sum( (log_ret.mean() * weights * 252))
        
        # Expected volatility
        vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov()*252, weights)))
        
        # Sharpe Ratio
        sharpe_arr[x] = ret_arr[x]/vol_arr[x]

    print('Max Sharpe ratio= {}'.format(sharpe_arr.max()))
    l = sharpe_arr.argmax()

    opt_weight = all_weights[l]

    max_sr_ret = ret_arr[sharpe_arr.argmax()]
    max_sr_vol = vol_arr[sharpe_arr.argmax()]

    inp2 = inp1
    inp2['Opt_weight'] = opt_weight
    inp2['Opt_value'] = inp2['Opt_weight']*np.sum(inp2['now_value'])
    inp2['Opt_quantity'] = (inp2['Opt_value']/inp2['ltp'])
    inp2['Opt_quantity'] = inp2['Opt_quantity'].astype(int)

    #optimized weightage and quantity
    print(inp2)

    #individual asset plot (portfolio1)
    portfolio1 = portfolio*100/portfolio.iloc[0]

    returns = portfolio.pct_change()
    returns = returns.iloc[1:]

    cov_matrix_annual = returns.cov() * 252

    #Original & Optimal Weights
    weight1 = inp1["Weightage"]
    weight2 = opt_weight
    #Portfolio Variance
    port_variance1 = np.dot(weight1.T, np.dot(cov_matrix_annual, weight1))
    port_variance2 = np.dot(weight2.T, np.dot(cov_matrix_annual, weight2))
    #Portfolio Volatility
    port_volatility1 = np.sqrt(port_variance1)
    port_volatility2 = np.sqrt(port_variance2)
    #Annual Return (CAGR)(both)
    portfolioSimpleAnnualReturn1 = np.sum(returns.mean()*weight1) * 252
    portfolioSimpleAnnualReturn2 = np.sum(returns.mean()*weight2) * 252

    percent_var1 = str(round(port_variance1, 2) * 100) + '%'
    percent_vols1 = str(round(port_volatility1, 2) * 100) + '%'
    percent_ret1 = str(round(portfolioSimpleAnnualReturn1, 2)*100)+'%'
    percent_var2 = str(round(port_variance2, 2) * 100) + '%'
    percent_vols2 = str(round(port_volatility2, 2) * 100) + '%'
    percent_ret2 = str(round(portfolioSimpleAnnualReturn2, 2)*100)+'%'
    print('Original Statistics ->')
    print("Expected annual return : "+ percent_ret1)
    print('Annual volatility/standard deviation/risk : '+percent_vols1)
    print('Annual variance : '+percent_var1)
    print('Optimized Statistics ->')
    print("Expected annual return : "+ percent_ret2)
    print('Annual volatility/standard deviation/risk : '+percent_vols2)
    print('Annual variance : '+percent_var2)



    #all variables to be added in this dictionary
    context = {
        "Current Value": net_now_value,
        "Invested value": net_buy_value,
        "Profit/loss": total_pnl,

    }


    # return inp1
    return render(request, 'product/portfolio.html', context)
