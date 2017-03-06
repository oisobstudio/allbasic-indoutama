# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apldistro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, unique=True, max_length=5)),
                ('name', models.CharField(max_length=50)),
                ('capital_price', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('keep', models.BooleanField(default=False)),
                ('brand', models.ForeignKey(to='apldistro.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(unique=True, max_length=5)),
                ('stock', models.PositiveIntegerField()),
                ('article', models.ForeignKey(to='aplinventory.Article')),
                ('brand', models.ForeignKey(to='apldistro.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='aplinventory/article')),
                ('article', models.ForeignKey(to='aplinventory.Article')),
                ('brand', models.ForeignKey(to='apldistro.Brand')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(unique=True, max_length=5)),
                ('name', models.CharField(max_length=30)),
                ('brand', models.ForeignKey(to='apldistro.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('brand', models.ForeignKey(to='apldistro.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5)),
                ('brand', models.ForeignKey(to='apldistro.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='SizeCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('brand', models.ForeignKey(to='apldistro.Brand')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='size',
            name='size_category',
            field=models.ForeignKey(to='aplinventory.SizeCategory'),
        ),
        migrations.AddField(
            model_name='size',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='sizecategory',
            field=models.ForeignKey(to='aplinventory.SizeCategory'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(to='aplinventory.ProductCategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articledetail',
            name='size',
            field=models.ForeignKey(to='aplinventory.Size'),
        ),
        migrations.AddField(
            model_name='articledetail',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='product',
            field=models.ForeignKey(to='aplinventory.Product'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='sizecategory',
            unique_together=set([('brand', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='size',
            unique_together=set([('name', 'size_category', 'brand')]),
        ),
        migrations.AlterUniqueTogether(
            name='articledetail',
            unique_together=set([('article', 'size')]),
        ),
    ]
