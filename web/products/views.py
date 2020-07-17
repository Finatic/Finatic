from django.shortcuts import render
from .forms import port_opti
from django.http import JsonResponse

#import libraries for function
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
    inp = pd.DataFrame(index = tick)
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
    for i in range(n):
        portfolio[ticker[i]] = pdr.DataReader(ticker[i].strip('\n'),data_source='yahoo',start = start_date, end = end_date)['Adj Close']
        now[ticker[i]] = pdr.DataReader(ticker[i].strip('\n'),data_source='yahoo',start = yester, end = today)['Adj Close']

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
    print('Current Value : ',net_now_value)
    print('Invested Value : ',net_buy_value)
    print('Profit / Loss : ',total_pnl)
    
    
    
    return render(request, 'product/portfolio.html', {} )