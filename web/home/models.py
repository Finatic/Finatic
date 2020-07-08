from django.db import models
import datetime

CHOICES = (
	('nifty 50','NIFTY 50'),
	('nifty 500','NIFTY 500'),
	('sensex','SENSEX'),
	)

# Create your models here.
class Home(models.Model):
	period = models.DecimalField(decimal_places=1,max_digits=500)
	start = models.DateField(default=datetime.date(1985,1,1))
	end = models.DateField(default=datetime.date.today)
	benchmark = models.CharField(max_length=10, choices = CHOICES, default ='NIFTY 50')
	

class Asset(models.Model):
	bse_code = models.CharField(max_length=10)
	name = models.CharField(max_length=25)
	quantity = models.DecimalField(decimal_places=0,max_digits=1000000)
	price = models.DecimalField(decimal_places=2, max_digits=1000000)

class Portfolio(models.Model):
	asset1 = models.ForeignKey(Asset, on_delete = models.CASCADE)


