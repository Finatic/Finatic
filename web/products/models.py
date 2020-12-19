from django.db import models
from django.contrib.auth.models import User
# Create your models here.


Portfolio_type_choice = (
    ('Asset Class', 'Asset Classes'),
    ('Tickers', 'Tickers'),
)
benchmark_choice = (
    ("NIFTY50", "NIFTY50"),
    ("SENSEX", "SENSEX"),
)

class MyPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MyPortfolio", null=True)
    portfolio_title = models.CharField(max_length=100, default="portfolio x")
    Portfolio_type = models.CharField(choices=Portfolio_type_choice, max_length=50, default="Tickers")
    benchmark = models.CharField(choices=benchmark_choice, max_length=20, default="SENSEX")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    number_of_portfolio = models.IntegerField(default=10)

    # ticker 1
    ticker_symbol_1 = models.CharField(max_length=50, null=True)
    quantity_1 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_1 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker 2
    ticker_symbol_2 = models.CharField(max_length=50, null=True)
    quantity_2 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_2 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_3
    ticker_symbol_3 = models.CharField(max_length=50, null=True)
    quantity_3 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_3 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_4
    ticker_symbol_4 = models.CharField(max_length=50, null=True)
    quantity_4 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_4 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_5
    ticker_symbol_5 = models.CharField(max_length=50, null=True)
    quantity_5 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_5 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_6
    ticker_symbol_6 = models.CharField(max_length=50, null=True)
    quantity_6 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_6 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_7
    ticker_symbol_7 = models.CharField(max_length=50, null=True)
    quantity_7 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_7 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_8
    ticker_symbol_8 = models.CharField(max_length=50, null=True)
    quantity_8 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_8 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_9
    ticker_symbol_9 = models.CharField(max_length=50, null=True)
    quantity_9 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_9 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_10
    ticker_symbol_10 = models.CharField(max_length=50, null=True)
    quantity_10 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_10 = models.DecimalField(decimal_places=2, max_digits=10, null=True)

    def __str__(self):
        return self.number_of_portfolio

class Port(models.Model):
    myport = models.ForeignKey(MyPortfolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.myport
