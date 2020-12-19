from django.shortcuts import render, redirect, reverse
from .forms import port_opti
from django.http import JsonResponse
from .solve2 import func1
from django.http import HttpResponseRedirect
from json import dumps
from .models import MyPortfolio, Port

# Create your views here.


def portfolio(response):
    message = []
    if response.method == 'POST':
        form = port_opti(response.POST)
 
        if form.is_valid():
            #form.save()
            portfolio_title = form.cleaned_data['portfolio_title']
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
            print(data)
            #form.data.save()

            nops = MyPortfolio(number_of_portfolio = nop, portfolio_title=portfolio_title, Portfolio_type=portfolio_type, start_date=start_date, end_date=end_date, benchmark=benchmark )
            nops.save()
            response.user.MyPortfolio.add(nops)

            context = {}
            context = func1(data, ticker_symbol, buy_price, quantity)

            # return HttpResponseRedirect(reverse(report, args=[context]))

            # return redirect('/products/report')
            return report(response, context)
            # return JsonResponse(data)

        else:
            error = form.errors.as_data()
            message.append(error)
            return render(response, 'home.html', {'message': message})
    else:
        form = port_opti
        data = []
        for i in range(1, 11):
            data.append(i)
        return render(response, 'product/portfolio.html', {'form': form, "number": data})


def report(response, context):
    return render(response, 'product/report.html', context)

def myports(response):
    return render(response, "myports.html")


            