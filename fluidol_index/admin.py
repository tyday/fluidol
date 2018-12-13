from django.contrib import admin
from .models import Product, Category, Product_benefits, Product_features, Product_applications
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Product_benefits)
admin.site.register(Product_features)
admin.site.register(Product_applications)
