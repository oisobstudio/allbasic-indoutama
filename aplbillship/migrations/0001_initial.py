# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apltransaction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(unique=True, max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('phone', models.CharField(max_length=30)),
                ('invoice', models.ForeignKey(to='apltransaction.Invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(unique=True, max_length=20)),
                ('province', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('vendor', models.CharField(max_length=100)),
                ('pack', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('price', models.IntegerField()),
                ('invoice', models.ForeignKey(to='apltransaction.Invoice')),
            ],
        ),
    ]
