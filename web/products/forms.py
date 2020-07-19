from django import forms
import datetime
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
    benchmark = forms.ChoiceField(choices=benchmark_choice)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField()
    number_of_portfolio = forms.IntegerField(max_value=10, min_value=1)

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
