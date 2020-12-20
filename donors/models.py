from django.db import models
from datetime import datetime





class Stock(models.Model):
    city = models.CharField(max_length=50)
    blood_type = models.CharField(max_length=20)
    exp_date = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.city + ' ' + self.blood_type