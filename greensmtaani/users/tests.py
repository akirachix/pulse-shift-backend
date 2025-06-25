from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Customer, MamaMboga, Address

class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="0712345678",
            password_hash="hash"
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertEqual(self.customer.email, "john.doe@example.com")
        self.assertTrue(self.customer.is_active)
        self.assertIsNotNone(self.customer.registration_date)

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "John Doe")

    def test_email_unique(self):
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                first_name="Jane",
                last_name="Smith",
                email="john.doe@example.com",  
                phone_number="0712345679",
                password_hash="hash"
            )

    def test_phone_unique(self):
        with self.assertRaises(IntegrityError):
            Customer.objects.create(
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                phone_number="0712345678",  
                password_hash="hash"
            )

    def test_max_length_fields(self):
        customer = Customer(
            first_name="A" * 256,  
            last_name="B" * 256,
            email="long.email@example.com",
            phone_number="1" * 21,
            password_hash="p" * 256
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()

class MamaMbogaModelTest(TestCase):
    def setUp(self):
        self.mama = MamaMboga.objects.create(
            kiosk_name="Test Kiosk",
            owner_first_name="Mama",
            owner_last_name="Mboga",
            email="mama@example.com",
            phone_number="0722222222",
            password_hash="hash"
        )

    def test_mama_creation(self):
        self.assertEqual(self.mama.kiosk_name, "Test Kiosk")
        self.assertEqual(self.mama.owner_first_name, "Mama")
        self.assertEqual(self.mama.owner_last_name, "Mboga")
        self.assertTrue(self.mama.is_active)
        self.assertIsNotNone(self.mama.registration_date)

    def test_mama_str(self):
        self.assertEqual(str(self.mama), "Test Kiosk")

    def test_email_unique(self):
        with self.assertRaises(IntegrityError):
            MamaMboga.objects.create(
                kiosk_name="Kiosk 2",
                owner_first_name="Other",
                owner_last_name="Owner",
                email="mama@example.com",  
                phone_number="0722222223",
                password_hash="hash"
            )

    def test_phone_unique(self):
        with self.assertRaises(IntegrityError):
            MamaMboga.objects.create(
                kiosk_name="Kiosk 3",
                owner_first_name="Other",
                owner_last_name="Owner",
                email="other@example.com",
                phone_number="0722222222",  
                password_hash="hash"
            )

    def test_nullable_fields(self):
        mama = MamaMboga.objects.create(
            kiosk_name="Null Kiosk",
            owner_first_name="Null",
            owner_last_name="Owner",
            email=None,
            phone_number="0722222224",
            password_hash="hash"
        )
        self.assertIsNone(mama.email)
        self.assertIsNone(mama.location_latitude)
        self.assertIsNone(mama.location_longitude)

class AddressModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Linda",
            last_name="Smith",
            email="linda@example.com",
            phone_number="0733333333",
            password_hash="hash"
        )

    def test_address_creation(self):
        address = Address.objects.create(
            customer=self.customer,
            is_default=True,
            latitude=-1.2921,
            longitude=36.8219
        )
        self.assertEqual(address.customer, self.customer)
        self.assertTrue(address.is_default)
        self.assertEqual(address.latitude, -1.2921)
        self.assertEqual(address.longitude, 36.8219)

    def test_cascade_delete(self):
        address = Address.objects.create(customer=self.customer)
        self.customer.delete()
        self.assertFalse(Address.objects.filter(pk=address.pk).exists())

    def test_multiple_addresses(self):
        Address.objects.create(customer=self.customer)
        Address.objects.create(customer=self.customer)
        self.assertEqual(self.customer.addresses.count(), 2)