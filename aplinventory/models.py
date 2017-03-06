from django.db import models
from apldistro.models import Brand


class SizeCategory(models.Model):
    user = models.ForeignKey('auth.User')
    brand = models.ForeignKey(Brand)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('brand', 'name')


class Size(models.Model):
    user = models.ForeignKey('auth.User')
    brand = models.ForeignKey(Brand)
    size_category = models.ForeignKey(SizeCategory)
    name = models.CharField(max_length=5)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        unique_together = ('name', 'size_category', 'brand')


class ProductCategory(models.Model):
    user = models.ForeignKey('auth.User')
    brand = models.ForeignKey(Brand)
    sizecategory = models.ForeignKey(SizeCategory)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey('auth.User')
    brand = models.ForeignKey(Brand)
    code = models.CharField(max_length=5, unique=True)
    product_category = models.ForeignKey(ProductCategory)
    name = models.CharField(max_length=30)

    def __str__(self):
        return "{} - {}".format(self.name, self.brand.name)


class Article(models.Model):
    user = models.ForeignKey('auth.User')
    brand = models.ForeignKey(Brand)
    product = models.ForeignKey(Product)
    code = models.CharField(max_length=5, unique=True, blank=True)
    name = models.CharField(max_length=50)
    capital_price = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    keep = models.BooleanField(default=False)

    def __str__(self):
        return "({}) - {}".format(self.code, self.name)


class ArticleDetail(models.Model):
    user = models.ForeignKey('auth.User')
    brand = models.ForeignKey(Brand)
    article = models.ForeignKey(Article)
    size = models.ForeignKey(Size)
    code = models.CharField(max_length=5, unique=True)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return "({}) - {}".format(self.code, self.article.name)

    class Meta:
        unique_together = ('article', 'size')


class Photo(models.Model):
    user = models.ForeignKey('auth.User')
    brand = models.ForeignKey(Brand)
    article = models.ForeignKey(Article)
    picture = models.ImageField(upload_to='aplinventory/article')

    def __str__(self):
        return self.article.name









