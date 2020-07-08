from django.contrib import admin

# Register your models here.
from .models import Home
from .models import Asset
from .models import Portfolio

admin.site.register(Home)
admin.site.register(Asset)
admin.site.register(Portfolio)