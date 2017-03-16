from django.db import models
from apltransaction.models import Invoice


class HoldTarget(models.Model):
	user = models.ForeignKey('auth.User')
	invoice_number = models.CharField(max_length=10, unique=True)
	state = models.IntegerField()
	record_date = models.DateField(auto_now_add=True)

	def __str__(self):
		return "({}) - {}".format(self.invoice_number, self.user.username)

# class ReasonPending(models.Model):

