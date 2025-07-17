from django.test import TestCase
from django.db import IntegrityError
from products.models import ProductCategory, Product

class ProductCategoryModelTests(TestCase):
    def setUp(self):
        self.category_data = {
            'category_name': 'Vegetables',
            'description': 'Fresh vegetables'
        }

    def test_create_category(self):
        category = ProductCategory.objects.create(**self.category_data)
        self.assertEqual(category.category_name, 'Vegetables')
        self.assertEqual(str(category), 'Vegetables')

    def test_unique_category_name(self):
        ProductCategory.objects.create(**self.category_data)
        with self.assertRaises(IntegrityError):
            ProductCategory.objects.create(**self.category_data)

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = ProductCategory.objects.create(category_name='Vegetables')
        self.product_data = {
            'name': 'Cabbage',
            'description': 'Fresh green cabbage',
            'category': self.category,
            'base_unit': 'kg',
            'image_url': 'http://example.com/cabbage.jpg'
        }

    def test_create_product(self):
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.name, 'Cabbage')
        self.assertEqual(str(product), 'Cabbage')