from django.db import models

from products.models import Product
from users.models import Address, Customer, MamaMboga


# Create your models here.
class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT) 
    order_date = models.DateTimeField(auto_now_add=True)
    customer_address = models.ForeignKey(Address, on_delete=models.RESTRICT, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_preference_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    current_status = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    expected_pickup_time = models.DateTimeField(null=True, blank=True)
    customer_feedback = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.customer} {self.order_id}"

        
class Order_items(models.Model):
    order_item_id=models.AutoField(primary_key=True)
    order= models.ForeignKey(Orders, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.RESTRICT)
    mama_mboga = models.ForeignKey(MamaMboga, on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)
    status_at_mama_mboga = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.order} {self.order_item_id}"

