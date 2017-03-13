from django.contrib import admin
from .models import SizeCategory, Article, ArticleDetail

class AdminArticleDetailInline(admin.TabularInline):
	model = ArticleDetail

class AdminArticle(admin.ModelAdmin):
	list_display = ('user', 'product', 'code', 'name', 'capital_price', 'price',)
	inlines = [
		AdminArticleDetailInline,
	]

admin.site.register(SizeCategory)
admin.site.register(Article, AdminArticle)
# Register your models here.
