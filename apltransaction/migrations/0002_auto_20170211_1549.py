# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apltransaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactiondetail',
            name='cut_price',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='transactiondetail',
            name='discount_code',
            field=models.CharField(null=True, max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='transactiondetail',
            name='discount_name',
            field=models.CharField(null=True, max_length=30, blank=True),
        ),
    ]
