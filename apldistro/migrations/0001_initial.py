# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('about', models.CharField(max_length=200, null=True, blank=True)),
                ('logo', models.ImageField(null=True, blank=True, upload_to='apldistro/brand/logo')),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('photo', models.ImageField(null=True, blank=True, upload_to='apldistro/profile')),
                ('level', models.CharField(max_length=1, default='A', choices=[('A', 'Admin'), ('W', 'Warehouse'), ('F', 'Founder'), ('M', 'Manager'), ('C', 'Cashier')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('founding_date', models.DateField()),
                ('about', models.CharField(max_length=200, null=True, blank=True)),
                ('logo', models.ImageField(null=True, blank=True, upload_to='apldistro/logo')),
                ('address', models.TextField(null=True, blank=True)),
                ('owner', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
