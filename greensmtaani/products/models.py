from django.db import models
from users.models import MamaMboga


class ProductCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    base_unit = models.CharField(max_length=50)
    image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StockRecord(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    mama_mboga = models.ForeignKey(MamaMboga, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, default="KES")
    current_stock_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    last_stock_update = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.mama_mboga} - {self.current_stock_quantity} {self.product.base_unit}"
