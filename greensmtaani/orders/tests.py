from django.test import TestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from decimal import Decimal
from users.models import Customer, MamaMboga, Address
from products.models import ProductCategory, Product
from orders.models import Orders, Order_items
from orders.serializers import OrdersSerializer, Order_itemsSerializer
class OrdersModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(first_name='John', last_name='Doe', email='john@example.com', phone_number='1234567890', password='securepassword')
        self.address = Address.objects.create(customer=self.customer, is_default=True, latitude=1.234, longitude=5.678, street_address='123 Main St', city='Nairobi')
        self.order_data = {'customer': self.customer, 'pickup_address': self.address, 'total_amount': Decimal('50.00'), 'current_status': 'Pending', 'payment_status': 'Unpaid'}
    def test_create_order(self):
        order = Orders.objects.create(**self.order_data)
        self.assertEqual(order.customer, self.customer)
class OrderItemsModelTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(first_name='John', last_name='Doe', email='john@example.com', phone_number='1234567890', password='securepassword')
        self.mama_mboga = MamaMboga.objects.create(kiosk_name='Veggie Stall', owner_first_name='Jane', owner_last_name='Doe', email='jane@example.com', phone_number='0987654321', password_hash='hashed_password')
        self.order = Orders.objects.create(customer=self.customer, total_amount=Decimal('50.00'), current_status='Pending', payment_status='Unpaid')
        self.category = ProductCategory.objects.create(category_name='Vegetables')
        self.product = Product.objects.create(name='Cabbage', category=self.category, base_unit='kg')
        self.order_item_data = {'order': self.order, 'product': self.product, 'mama_mboga': self.mama_mboga, 'quantity': Decimal('2.00'), 'price_per_unit_at_order': Decimal('10.50'), 'item_total': Decimal('21.00')}
    def test_create_order_item(self):
        order_item = Order_items.objects.create(**self.order_item_data)
        self.assertEqual(order_item.order, self.order)






