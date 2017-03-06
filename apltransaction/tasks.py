
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .models import TransactionDetail, Invoice
from .utils import remove_invoicestore_hold0
logger = get_task_logger(__name__)



@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="periodic_task_delete_invoicestore_status_hold0",
    ignore_result=True
)
def periodic_task_delete_invoicestore_status_hold0():
    remove_invoicestore_hold0()
    logger.info("remove invoices !")
