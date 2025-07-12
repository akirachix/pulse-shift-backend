from django.contrib import admin


from .models import Product, ProductCategory, StockRecord

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(StockRecord)

