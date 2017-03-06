from .models import TransactionDetail, Invoice

def remove_invoicestore_hold0():
    invoices = Invoice.objects.filter(status='H')


    for invoice in invoices:
        if invoice.transactiondetail_set.count() <= 0:
            invoice.delete()
