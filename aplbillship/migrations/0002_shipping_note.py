# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplbillship', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]
