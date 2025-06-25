from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Customer, MamaMboga, Address

class CustomerAPITestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Alice",
            last_name="Wonderland",
            email="alice@example.com",
            phone_number="0711111111",
            password_hash="hash"
        )
        self.list_url = reverse('customers-list')

    def test_customer_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Customer.objects.count())
        self.assertEqual(response.data[0]['email'], self.customer.email)

    def test_customer_create(self):
        data = {
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "bob@example.com",
            "phone_number": "0722222222",
            "password_hash": "hash"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Customer.objects.filter(email="bob@example.com").exists())

    def test_customer_unique_email(self):
        data = {
            "first_name": "Charlie",
            "last_name": "Chaplin",
            "email": "alice@example.com",  # Duplicate
            "phone_number": "0733333333",
            "password_hash": "hash"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class MamaMbogaAPITestCase(APITestCase):
    def setUp(self):
        self.mama = MamaMboga.objects.create(
            kiosk_name="Mama's Place",
            owner_first_name="Mama",
            owner_last_name="Mboga",
            email="mama@mboga.com",
            phone_number="0744444444",
            password_hash="hash"
        )
        self.list_url = reverse('mama-mbogas-list')

    def test_mama_mboga_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), MamaMboga.objects.count())

    def test_mama_mboga_create(self):
        data = {
            "kiosk_name": "New Kiosk",
            "owner_first_name": "New",
            "owner_last_name": "Owner",
            "email": "new@kiosk.com",
            "phone_number": "0755555555",
            "password_hash": "hash"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mama_mboga_unique_email(self):
        data = {
            "kiosk_name": "Another",
            "owner_first_name": "Dup",
            "owner_last_name": "Owner",
            "email": "mama@mboga.com",  # Duplicate
            "phone_number": "0756666666",
            "password_hash": "hash"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AddressAPITestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Dave",
            last_name="Jones",
            email="dave@example.com",
            phone_number="0766666666",
            password_hash="hash"
        )
        self.address = Address.objects.create(
            customer=self.customer,
            is_default=True,
            latitude=-1.2921,
            longitude=36.8219
        )
        self.list_url = reverse('addresses-list')

    def test_address_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Address.objects.count())

    def test_address_create(self):
        data = {
            "customer": self.customer.pk,
            "is_default": False,
            "latitude": 0.0,
            "longitude": 0.0
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Address.objects.filter(latitude=0.0, longitude=0.0).exists())

    def test_address_requires_customer(self):
        data = {
            "is_default": True,
            "latitude": 1.1,
            "longitude": 2.2
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)