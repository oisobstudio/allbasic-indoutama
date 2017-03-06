# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('invoice_number', models.CharField(unique=True, max_length=10)),
                ('invoice_date', models.DateField(default=datetime.date.today)),
                ('total', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('abbv', models.CharField(max_length=2)),
                ('info', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('abbv', models.CharField(max_length=2)),
                ('info', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('article_brand_code', models.CharField(max_length=30)),
                ('article_brand_name', models.CharField(max_length=100)),
                ('article_code', models.CharField(max_length=200)),
                ('article_name', models.CharField(max_length=200)),
                ('article_size', models.CharField(max_length=50)),
                ('article_price', models.PositiveIntegerField()),
                ('article_capitalprice', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('sub_total', models.PositiveIntegerField()),
                ('invoice', models.ForeignKey(to='apltransaction.Invoice')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='category',
            field=models.ForeignKey(to='apltransaction.InvoiceCategory'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.ForeignKey(to='apltransaction.InvoiceStatus'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='transactiondetail',
            unique_together=set([('invoice', 'article_size', 'article_code')]),
        ),
    ]
