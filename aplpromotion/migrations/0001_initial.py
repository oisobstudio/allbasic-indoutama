# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apltransaction', '0002_auto_20170211_1549'),
        ('aplinventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=30)),
                ('cut_price', models.PositiveIntegerField()),
                ('article', models.ForeignKey(to='aplinventory.Article')),
                ('place', models.ForeignKey(to='apltransaction.InvoiceCategory')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='discount',
            unique_together=set([('article', 'place')]),
        ),
    ]
