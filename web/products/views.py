from django.shortcuts import render
from .forms import port_opti
from django.http import JsonResponse

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

            input_data = {}
            input_data['ticker'] = ticker_symbol
            input_data['quantity'] = quantity
            input_data['buy'] = buy_price
            print(input_data)
            print(ticker_symbol)
            print(buy_price)
            print(quantity)
            data = form.cleaned_data
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
