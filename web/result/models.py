from django.db import models

# Trial model (TEMPORARY)
class outputa(models.Model):
    ltp = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()

    def __float__(self):
        return self.ltp