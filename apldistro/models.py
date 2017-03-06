from django.db import models


class Store(models.Model):
    code = models.CharField(max_length=100, unique=True)
    owner = models.OneToOneField('auth.User')
    name = models.CharField(max_length=100)
    founding_date = models.DateField()
    about = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to='apldistro/logo', blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to='apldistro/brand/logo', blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    LEVEL_PROFILE = (
        ('A', 'Admin'),
        ('W', 'Warehouse'),
        ('F', 'Founder'),
        ('M', 'Manager'),
        ('C', 'Cashier'),
    )

    user = models.OneToOneField('auth.User')
    photo = models.ImageField(upload_to='apldistro/profile', blank=True, null=True)
    level = models.CharField(max_length=1, choices=LEVEL_PROFILE, default='A')

    def __str__(self):
        return self.user.username


