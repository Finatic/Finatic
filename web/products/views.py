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
            ticker_symbol = form.cleaned_data['ticker_symbol']
            quantity = form.cleaned_data['quantity']
            buy_price = form.cleaned_data['buy_price']
            print(portfolio_type, " ", start_date, " ", ticker_symbol)
            print(form.data)
            print(form.__dict__)
            data = form.cleaned_data
            return JsonResponse(data)

        else:
            print(form.errors.as_data())

        return render(request, 'home.html', {'message': message})
    else:
        form = port_opti
        data = []
        for i in range(1):
            data.append(i)
        return render(request, 'product/portfolio.html', {'form': form, "number": data})
