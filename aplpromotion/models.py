from django.db import models
from aplinventory.models import Article
from apltransaction.models import InvoiceCategory


class Discount(models.Model):
	code = models.CharField(max_length=10, unique=True)
	article = models.ForeignKey(Article)
	place = models.ForeignKey(InvoiceCategory)
	name = models.CharField(max_length=30)
	cut_price = models.PositiveIntegerField()

	class Meta:
		unique_together = ('article', 'place')

	def __str__(self):
		return self.name


