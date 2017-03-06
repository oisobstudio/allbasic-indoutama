from django import forms
from .models import SizeCategory, Size, ProductCategory, \
    Product, Article, ArticleDetail
from aplhelper.helpers import helper_session_brand_pk
from apldistro.models import Brand


class FormSizeCategoryAdd(forms.ModelForm):
    class Meta:
        model = SizeCategory
        fields = ('name',)


class FormSizeCategoryChange(forms.ModelForm):
    class Meta:
        model = SizeCategory
        fields = ('name',)


class FormAddSize(forms.ModelForm):

    class Meta:
        model = Size
        fields = ('name',)


class FormChangeSize(forms.ModelForm):

    class Meta:
        model = Size
        fields = ('name',)


class FormAddProductCategory(forms.ModelForm):
    def __init__(self, brand, *args, **kwargs):
        super(FormAddProductCategory, self).__init__(*args, **kwargs)
        self.fields['sizecategory'].queryset = SizeCategory.objects.filter(brand=brand)

    class Meta:
        model = ProductCategory
        fields = ('name', 'sizecategory')


class FormChangeProductCategory(forms.ModelForm):
    def __init__(self, brand, *args, **kwargs):
        super(FormChangeProductCategory, self).__init__(*args, **kwargs)
        self.fields['sizecategory'].queryset = SizeCategory.objects.filter(brand=brand)

    class Meta:
        model = ProductCategory
        fields = ('name', 'sizecategory')


class FormAddProduct(forms.ModelForm):

    def __init__(self, brand, *args, **kwargs):
        super(FormAddProduct, self).__init__(*args, **kwargs)
        self.fields['product_category'].queryset = ProductCategory.objects.filter(brand=brand)

    class Meta:
        model = Product
        fields = ('product_category', 'name')


class FormChangeProduct(forms.ModelForm):
    def __init__(self, brand, *args, **kwargs):
        super(FormChangeProduct, self).__init__(*args, **kwargs)
        self.fields['product_category'].queryset = ProductCategory.objects.filter(brand=brand)

    class Meta:
        model = Product
        fields = ('product_category', 'name')


class FormAddArticle(forms.ModelForm):


    def __init__(self, brand, *args, **kwargs):
        super(FormAddArticle, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(brand=brand)

    class Meta:
        model = Article
        fields = ['product', 'name', 'capital_price', 'price']
        

class FormChangeArticle(forms.ModelForm):

    
    class Meta:
        model = Article
        fields = ['name', 'capital_price', 'price']

        
class FormAddArticleDetail(forms.ModelForm):

    def __init__(self, sizes, *args, **kwargs):
        super(FormAddArticleDetail, self).__init__(*args, **kwargs)
        self.fields['size'].queryset = sizes

    class Meta:
        model = ArticleDetail
        fields = ['stock', 'size']
        
    
class FormChangeArticleDetail(forms.ModelForm):
    
    def __init__(self, brand, sizecategory, *args, **kwargs):
        super(FormChangeArticleDetail, self).__init__(*args, **kwargs)
        self.fields['size'].queryset = Size.objects.filter(brand=brand, size_category=sizecategory)
    
    class Meta:
        model = ArticleDetail
        fields = ('stock', 'size')


class FormSearchProduct(forms.Form):
    query = forms.CharField()

