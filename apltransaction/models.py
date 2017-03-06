from django.db import models
from apldistro.models import Brand
from aplinventory.models import ArticleDetail
import datetime

class InvoiceCategory(models.Model):
    abbv = models.CharField(max_length=2)
    info = models.CharField(max_length=30)

    def __str__(self):
        return self.abbv


class InvoiceStatus(models.Model):
    abbv = models.CharField(max_length=2)
    info = models.CharField(max_length=30)

    def __str__(self):
        return self.abbv


class Invoice(models.Model):
    user = models.ForeignKey('auth.User')
    invoice_number = models.CharField(max_length=10, unique=True)
    invoice_date = models.DateField(default=datetime.date.today)
    total = models.PositiveIntegerField()
    category = models.ForeignKey(InvoiceCategory)
    status = models.ForeignKey(InvoiceStatus)

    def __str__(self):
        return self.invoice_number


class TransactionDetail(models.Model):
    user = models.ForeignKey('auth.User')
    invoice = models.ForeignKey(Invoice)

    article_brand_code = models.CharField(max_length=30)
    article_brand_name = models.CharField(max_length=100)
    article_code = models.CharField(max_length=200)
    article_name = models.CharField(max_length=200)
    article_size = models.CharField(max_length=50)
    article_price = models.PositiveIntegerField()
    article_capitalprice = models.PositiveIntegerField()

    quantity = models.PositiveIntegerField()
    sub_total = models.PositiveIntegerField()
    
    ################ DISCOUNT AREA #########################################
    discount_code = models.CharField(max_length=100, blank=True, null=True)
    discount_name = models.CharField(max_length=30, blank=True, null=True)
    cut_price = models.PositiveIntegerField(blank=True, null=True)
    ########################################################################

    def __str__(self):
        return self.invoice.invoice_number

    class Meta:
        unique_together = ('invoice', 'article_size', 'article_code')





