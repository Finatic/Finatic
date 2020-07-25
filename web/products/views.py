from django.shortcuts import render, redirect, reverse
from .forms import port_opti
from django.http import JsonResponse
from .solve import func1
from django.http import HttpResponseRedirect
from json import dumps


# Create your views here.


def portfolio(request):
    message = []
    if request.method == 'POST':
        form = port_opti(request.POST)

        if form.is_valid():
            # portfolio_type = form.cleaned_data['Portfolio_type']
            # start_date = form.cleaned_data['start_date']
            # end_date = form.cleaned_data['end_date']
            nop = form.cleaned_data['number_of_portfolio']
            # benchmark = form.cleaned_data['benchmark']
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
            context = {}
            context = func1(data, ticker_symbol, buy_price, quantity)

            # return HttpResponseRedirect(reverse(report, args=[context]))

            # return redirect('/products/report')
            return report(request, context)
            # return JsonResponse(data)

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


def report(request, context):
    return render(request, 'product/report.html', context)
