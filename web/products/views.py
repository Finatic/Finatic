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
            data = form.cleaned_data
            return JsonResponse(data)

        else:
            error = form.errors.as_data()
            message.append(error)
            return render(request, 'home.html', {'message': message})
    else:
        form = port_opti
        data = []
        for i in range(2):
            data.append(i)
        return render(request, 'product/portfolio.html', {'form': form, "number": data})
