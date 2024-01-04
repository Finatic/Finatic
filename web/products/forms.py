from django import forms
import datetime
from .models import MyPortfolio
# port opti variable

Portfolio_type_choice = (
    ('Asset Class', 'Asset Classes'),
    ('Tickers', 'Tickers'),
)
Time_period_choice = (
    ("1", 'year to year'),
    ('2', "month to month"),
)
start_year_choice = []
for i in range(1985, 2021):
    start_year_choice.append((i, i))

month_choice = (
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),

)
Optimization_goal_choice = (
    ("1", "Maximize Sharpe Ratio"),
    ("2", "Minimize Volatility subject to..."),
    ("3", "Maximize Return subject to..."),
    ("4", "Minimize Variance"),
    ("5", "Minimize Conditional Value-at-Risk"),
    ("6", "Risk Parity"),
    ("7", "Minimize Tracking Error"),
    ("8", "Maximize Information Ratio"),
    ("9", "Minimize Maximum Drawdown subject to..."),
    ("10", "Maximize Omega Ratio subject to..."),
    ("11", "Maximize Sortino Ratio subject to..."),

)
benchmark_choice = (
    ("NIFTY50", "NIFTY50"),
    ("SENSEX", "SENSEX"),
)



class port_opti(forms.Form):
    
    Portfolio_type = forms.ChoiceField(
        choices=Portfolio_type_choice, required=False)
    portfolio_title = forms.CharField(max_length=500, required=False)
    benchmark = forms.ChoiceField(choices=benchmark_choice)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    number_of_portfolio = forms.IntegerField(max_value=30, min_value=1)

    # ticker 1
    ticker_symbol_1 = forms.CharField(required=False)
    quantity_1 = forms.DecimalField(required=False)
    buy_price_1 = forms.DecimalField(required=False)
    # ticker 2
    ticker_symbol_2 = forms.CharField(required=False)
    quantity_2 = forms.DecimalField(required=False)
    buy_price_2 = forms.DecimalField(required=False)
    # ticker_3
    ticker_symbol_3 = forms.CharField(required=False)
    quantity_3 = forms.DecimalField(required=False)
    buy_price_3 = forms.DecimalField(required=False)
    # ticker_4
    ticker_symbol_4 = forms.CharField(required=False)
    quantity_4 = forms.DecimalField(required=False)
    buy_price_4 = forms.DecimalField(required=False)
    # ticker_5
    ticker_symbol_5 = forms.CharField(required=False)
    quantity_5 = forms.DecimalField(required=False)
    buy_price_5 = forms.DecimalField(required=False)
    # ticker_6
    ticker_symbol_6 = forms.CharField(required=False)
    quantity_6 = forms.DecimalField(required=False)
    buy_price_6 = forms.DecimalField(required=False)
    # ticker_7
    ticker_symbol_7 = forms.CharField(required=False)
    quantity_7 = forms.DecimalField(required=False)
    buy_price_7 = forms.DecimalField(required=False)
    # ticker_8
    ticker_symbol_8 = forms.CharField(required=False)
    quantity_8 = forms.DecimalField(required=False)
    buy_price_8 = forms.DecimalField(required=False)
    # ticker_9
    ticker_symbol_9 = forms.CharField(required=False)
    quantity_9 = forms.DecimalField(required=False)
    buy_price_9 = forms.DecimalField(required=False)
    # ticker_10
    ticker_symbol_10 = forms.CharField(required=False)
    quantity_10 = forms.DecimalField(required=False)
    buy_price_10 = forms.DecimalField(required=False)
    # ticker 11
    ticker_symbol_11 = forms.CharField(required=False)
    quantity_11= forms.DecimalField(required=False)
    buy_price_11 = forms.DecimalField(required=False)
    # ticker 12
    ticker_symbol_12 = forms.CharField(required=False)
    quantity_12 = forms.DecimalField(required=False)
    buy_price_12 = forms.DecimalField(required=False)
    # ticker_13
    ticker_symbol_13 = forms.CharField(required=False)
    quantity_13 = forms.DecimalField(required=False)
    buy_price_13 = forms.DecimalField(required=False)
    # ticker_14
    ticker_symbol_14 = forms.CharField(required=False)
    quantity_14 = forms.DecimalField(required=False)
    buy_price_14 = forms.DecimalField(required=False)
    # ticker_15
    ticker_symbol_15 = forms.CharField(required=False)
    quantity_15 = forms.DecimalField(required=False)
    buy_price_15 = forms.DecimalField(required=False)
    # ticker_16
    ticker_symbol_16 = forms.CharField(required=False)
    quantity_16 = forms.DecimalField(required=False)
    buy_price_16 = forms.DecimalField(required=False)
    # ticker_17
    ticker_symbol_17 = forms.CharField(required=False)
    quantity_17 = forms.DecimalField(required=False)
    buy_price_17 = forms.DecimalField(required=False)
    # ticker_18
    ticker_symbol_18 = forms.CharField(required=False)
    quantity_18 = forms.DecimalField(required=False)
    buy_price_18 = forms.DecimalField(required=False)
    # ticker_19
    ticker_symbol_19 = forms.CharField(required=False)
    quantity_19 = forms.DecimalField(required=False)
    buy_price_19 = forms.DecimalField(required=False)
    # ticker_20
    ticker_symbol_20 = forms.CharField(required=False)
    quantity_20 = forms.DecimalField(required=False)
    buy_price_20 = forms.DecimalField(required=False)
    # ticker 21
    ticker_symbol_21 = forms.CharField(required=False)
    quantity_21 = forms.DecimalField(required=False)
    buy_price_21 = forms.DecimalField(required=False)
    # ticker 22
    ticker_symbol_22 = forms.CharField(required=False)
    quantity_22 = forms.DecimalField(required=False)
    buy_price_22 = forms.DecimalField(required=False)
    # ticker_23
    ticker_symbol_23 = forms.CharField(required=False)
    quantity_23 = forms.DecimalField(required=False)
    buy_price_23 = forms.DecimalField(required=False)
    # ticker_4
    ticker_symbol_24 = forms.CharField(required=False)
    quantity_24 = forms.DecimalField(required=False)
    buy_price_24 = forms.DecimalField(required=False)
    # ticker_25
    ticker_symbol_25 = forms.CharField(required=False)
    quantity_25 = forms.DecimalField(required=False)
    buy_price_25 = forms.DecimalField(required=False)
    # ticker_26
    ticker_symbol_26 = forms.CharField(required=False)
    quantity_26 = forms.DecimalField(required=False)
    buy_price_26 = forms.DecimalField(required=False)
    # ticker_27
    ticker_symbol_27 = forms.CharField(required=False)
    quantity_27 = forms.DecimalField(required=False)
    buy_price_27 = forms.DecimalField(required=False)
    # ticker_28
    ticker_symbol_28 = forms.CharField(required=False)
    quantity_28 = forms.DecimalField(required=False)
    buy_price_28 = forms.DecimalField(required=False)
    # ticker_29
    ticker_symbol_29 = forms.CharField(required=False)
    quantity_29 = forms.DecimalField(required=False)
    buy_price_29 = forms.DecimalField(required=False)
    # ticker_30
    ticker_symbol_30 = forms.CharField(required=False)
    quantity_30 = forms.DecimalField(required=False)
    buy_price_30 = forms.DecimalField(required=False)

    # Time_period = forms.ChoiceField(choices=Time_period_choice, widget=forms.Select(
    #     attrs={'class': 'form-control', 'onchange': 'toggleTimeframe()'}))
    # start_year = forms.ChoiceField(choices=start_year_choice, widget=forms.Select(
    #     attrs={'class': 'form-control', 'onchange': 'toggleTimeframe()'}))
    # end_year = forms.ChoiceField(choices=start_year_choice, widget=forms.Select(
    #     attrs={'class': 'form-control', 'onchange': 'toggleTimeframe()'}))
    # start_month = forms.ChoiceField(choices=month_choice, widget=forms.Select(
    #     attrs={'class': 'form-control ', 'onchange': 'toggleTimeframe()'}))
    # end_month = forms.ChoiceField(choices=month_choice, widget=forms.Select(
    #     attrs={'class': 'form-control', 'onchange': 'toggleTimeframe()'}))
    # Optimization_goal = forms.ChoiceField(
    #     choices=Optimization_goal_choice, widget=forms.Select(
    #         attrs={'class': 'form-control', 'onchange': 'toggleTimeframe()'}))
