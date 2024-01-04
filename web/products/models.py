from django.db import models
from django.contrib.auth.models import User
# Create your models here.


Portfolio_type_choice = (
    ('Asset Class', 'Asset Classes'),
    ('Tickers', 'Tickers'),
)
benchmark_choice = (
    ("NIFTY500", "NIFTY500"),
    ("SENSEX", "SENSEX"),
)

class MyPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MyPortfolio", null=True)
    portfolio_title = models.CharField(max_length=100, default="portfolio x")
    Portfolio_type = models.CharField(choices=Portfolio_type_choice, max_length=50, default="Tickers")
    benchmark = models.CharField(choices=benchmark_choice, max_length=20, default="SENSEX")
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    number_of_portfolio = models.IntegerField(default=30)

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
    # ticker 11
    ticker_symbol_11 = models.CharField(max_length=50, null=True)
    quantity_11 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_11 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker 12
    ticker_symbol_12 = models.CharField(max_length=50, null=True)
    quantity_12 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_12 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_13
    ticker_symbol_13 = models.CharField(max_length=50, null=True)
    quantity_13 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_13 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_14
    ticker_symbol_14 = models.CharField(max_length=50, null=True)
    quantity_14 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_14 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_15
    ticker_symbol_15 = models.CharField(max_length=50, null=True)
    quantity_15 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_15 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_16
    ticker_symbol_16 = models.CharField(max_length=50, null=True)
    quantity_16 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_16 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_17
    ticker_symbol_17 = models.CharField(max_length=50, null=True)
    quantity_17 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_17 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_18
    ticker_symbol_18 = models.CharField(max_length=50, null=True)
    quantity_18 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_18 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_19
    ticker_symbol_19 = models.CharField(max_length=50, null=True)
    quantity_19 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_19 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_20
    ticker_symbol_20 = models.CharField(max_length=50, null=True)
    quantity_20 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_20 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker 21
    ticker_symbol_21 = models.CharField(max_length=50, null=True)
    quantity_21 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_21 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker 22
    ticker_symbol_22 = models.CharField(max_length=50, null=True)
    quantity_22 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_22 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_23
    ticker_symbol_23 = models.CharField(max_length=50, null=True)
    quantity_23 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_23 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_24
    ticker_symbol_24 = models.CharField(max_length=50, null=True)
    quantity_24 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_24 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_25
    ticker_symbol_25 = models.CharField(max_length=50, null=True)
    quantity_25 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_25 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_26
    ticker_symbol_26 = models.CharField(max_length=50, null=True)
    quantity_26 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_26 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_27
    ticker_symbol_27 = models.CharField(max_length=50, null=True)
    quantity_27 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_27 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_28
    ticker_symbol_28 = models.CharField(max_length=50, null=True)
    quantity_28 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_28 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_29
    ticker_symbol_29 = models.CharField(max_length=50, null=True)
    quantity_29 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_29 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    # ticker_30
    ticker_symbol_30 = models.CharField(max_length=50, null=True)
    quantity_30 = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    buy_price_30 = models.DecimalField(decimal_places=2, max_digits=10, null=True)

    def __str__(self):
        return self.number_of_portfolio

class Port(models.Model):
    myport = models.ForeignKey(MyPortfolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.myport
