from django.forms import ModelForm
from models import Home

class TickerForm(ModelForm):
    class Meta:
        model = Home
        fields = ['period','start','end','benchmark']

