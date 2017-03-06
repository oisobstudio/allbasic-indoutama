from django.db import models
from apltransaction.models import Invoice


class Billing(models.Model):
    code = models.CharField(max_length=20, unique=True)
    invoice = models.ForeignKey(Invoice)
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.code


class Shipping(models.Model):
    code = models.CharField(unique=True, max_length=20)
    invoice = models.ForeignKey(Invoice)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    pack = models.CharField(max_length=100)
    address = models.TextField()
    price = models.IntegerField()
    note = models.TextField(blank=True)
