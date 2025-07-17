
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from decimal import Decimal
from users.models import Customer, MamaMboga
from orders.models import Orders
from payments.models import Payment, Payout

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def customer(db):
    return Customer.objects.create(
        first_name="Johnny", last_name="Deedy", phone_number="0712345678"
    )

@pytest.fixture
def mama_mboga(db):
    return MamaMboga.objects.create(
        kiosk_name="Mama's Veggies", phone_number="0712345670"
    )

@pytest.fixture
def order(db, customer):
    return Orders.objects.create(
        customer=customer,
        total_amount=Decimal("500.00"),
        order_preference_fee=Decimal("0.00"),
        current_status="PENDING",
        payment_status="PENDING"
    )

@pytest.fixture
def payment(db, customer, order):
    return Payment.objects.create(
        order=order,
        customer=customer,
        total_amount=Decimal("200.00"),
        phone_number="0712345678",
        status="SUCCESS"
    )

@pytest.fixture
def payout(db, mama_mboga):
    return Payout.objects.create(
        mama_mboga=mama_mboga,
        amount=Decimal("300.00"),
        status="PENDING"
    )

@pytest.mark.django_db
def test_create_payment(api_client, customer, order):
    url = reverse('payment-list')
    data = {
        "order": order.id,
        "customer": customer.id,
        "total_amount": "150.00",
        "phone_number": "0712345678",
        "status": "PENDING"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert float(response.data["total_amount"]) == 150.00
    assert response.data["status"] == "PENDING"

@pytest.mark.django_db
def test_get_payment(api_client, payment):
    url = reverse('payment-detail', args=[payment.pk])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["payment_id"] == payment.pk

@pytest.mark.django_db
def test_list_payments(api_client, payment):
    url = reverse('payment-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, list) or "results" in response.data

@pytest.mark.django_db
def test_update_payment(api_client, payment, order, customer):
    url = reverse('payment-detail', args=[payment.pk])
    data = {
        "order": order.id,
        "customer": customer.id,
        "total_amount": "333.33",
        "phone_number": "0700000000",
        "status": "FAILED"
    }
    response = api_client.put(url, data, format="json")
    assert response.status_code in [200, 202]  
    assert float(response.data["total_amount"]) == 333.33
    assert response.data["status"] == "FAILED"
    assert response.data["phone_number"] == "0700000000"

@pytest.mark.django_db
def test_delete_payment(api_client, payment):
    url = reverse('payment-detail', args=[payment.pk])
    response = api_client.delete(url)
    assert response.status_code == 204
    get_response = api_client.get(url)
    assert get_response.status_code == 404

@pytest.mark.django_db
def test_invalid_payment_missing_fields(api_client):
    url = reverse('payment-list')
    data = {
        "phone_number": "0712345678",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "order" in response.data
    assert "customer" in response.data
    assert "total_amount" in response.data

@pytest.mark.django_db
def test_create_payout(api_client, mama_mboga):
    url = reverse('payout-list')
    data = {
        "mama_mboga": mama_mboga.id,
        "amount": "300.00",
        "status": "PENDING"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert float(response.data["amount"]) == 300.00
    assert response.data["status"] == "PENDING"

@pytest.mark.django_db
def test_get_payout(api_client, payout):
    url = reverse('payout-detail', args=[payout.pk])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["payout_id"] == payout.pk

@pytest.mark.django_db
def test_list_payouts(api_client, payout):
    url = reverse('payout-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, list) or "results" in response.data

@pytest.mark.django_db
def test_update_payout(api_client, payout, mama_mboga):
    url = reverse('payout-detail', args=[payout.pk])
    data = {
        "mama_mboga": mama_mboga.id,
        "amount": "999.99",
        "status": "SUCCESS",
        "payout_method": "BANK"
    }
    response = api_client.put(url, data, format="json")
    assert response.status_code in [200, 202]
    assert float(response.data["amount"]) == 999.99
    assert response.data["status"] == "SUCCESS"
    assert response.data["payout_method"] == "BANK"

@pytest.mark.django_db
def test_delete_payout(api_client, payout):
    url = reverse('payout-detail', args=[payout.pk])
    response = api_client.delete(url)
    assert response.status_code == 204
    get_response = api_client.get(url)
    assert get_response.status_code == 404

@pytest.mark.django_db
def test_invalid_payout_missing_fields(api_client):
    url = reverse('payout-list')
    data = {
        "amount": "100.00",
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
    assert "mama_mboga" in response.data


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Customer, MamaMboga, Address
from nutrition.models import DietaryPreference, MealPlan
import datetime

class DietaryPreferenceAPITestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            phone_number="0712345678",
            password="supersecret"
        )
        self.pref_data = {
            "customer": self.customer.pk,
            "dietary_type": "Vegan",
            "excluded_ingredients": ["peanuts", "gluten"],
            "favorite_cuisines": ["Italian", "Indian"],
            "preferred_meal_types": ["breakfast", "dinner"],
            "nutritional_goal": "High Protein"
        }

    def test_create_dietary_preference(self):
        url = reverse('dietary-preferences-list')
        response = self.client.post(url, self.pref_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DietaryPreference.objects.count(), 1)
        pref = DietaryPreference.objects.get()
        self.assertEqual(pref.customer, self.customer)
        self.assertEqual(pref.dietary_type, "Vegan")
        self.assertListEqual(pref.excluded_ingredients, ["peanuts", "gluten"])
        self.assertListEqual(pref.favorite_cuisines, ["Italian", "Indian"])
        self.assertListEqual(pref.preferred_meal_types, ["breakfast", "dinner"])
        self.assertEqual(pref.nutritional_goal, "High Protein")

    def test_blank_array_fields(self):
        url = reverse('dietary-preferences-list')
        data = {
            "customer": self.customer.pk,
            "dietary_type": "Vegetarian",
            "nutritional_goal": "Balanced"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pref = DietaryPreference.objects.get()
        self.assertEqual(pref.excluded_ingredients, [])
        self.assertEqual(pref.favorite_cuisines, [])
        self.assertEqual(pref.preferred_meal_types, [])

    def test_list_dietary_preferences(self):
        DietaryPreference.objects.create(
            customer=self.customer,
            dietary_type="Vegan",
            excluded_ingredients=["peanuts", "gluten"],
            favorite_cuisines=["Italian", "Indian"],
            preferred_meal_types=["breakfast", "dinner"],
            nutritional_goal="High Protein"
        )
        url = reverse('dietary-preferences-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class MealPlanAPITestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            phone_number="0712345678",
            password="supersecret"
        )
        self.preference = DietaryPreference.objects.create(
            customer=self.customer,
            dietary_type="Keto",
            nutritional_goal="Low Carb"
        )
        self.start_date = datetime.date.today()
        self.end_date = self.start_date + datetime.timedelta(days=7)
        self.plan_data = {
            "customer": self.customer.pk,
            "name": "Weekly Keto Plan",
            "start_date": self.start_date,
            "end_date": self.end_date,
            "is_active": True,
            "base_preference": self.preference.pk,
            "version": 1
        }

    def test_create_meal_plan(self):
        url = reverse('meal-plans-list')
        response = self.client.post(url, self.plan_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MealPlan.objects.count(), 1)
        plan = MealPlan.objects.get()
        self.assertEqual(plan.customer, self.customer)
        self.assertEqual(plan.name, "Weekly Keto Plan")
        self.assertEqual(plan.start_date, self.start_date)
        self.assertEqual(plan.end_date, self.end_date)
        self.assertTrue(plan.is_active)
        self.assertEqual(plan.base_preference, self.preference)
        self.assertEqual(plan.version, 1)

    def test_meal_plan_without_preference(self):
        url = reverse('meal-plans-list')
        data = {
            "customer": self.customer.pk,
            "name": "Short Plan",
            "start_date": self.start_date,
            "end_date": self.start_date + datetime.timedelta(days=3)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        plan = MealPlan.objects.get()
        self.assertIsNone(plan.base_preference)
        self.assertTrue(plan.is_active)
        self.assertEqual(plan.version, 1)

    def test_list_meal_plans(self):
        MealPlan.objects.create(
            customer=self.customer,
            name="Weekly Keto Plan",
            start_date=self.start_date,
            end_date=self.end_date,
            is_active=True,
            base_preference=self.preference,
            version=1
        )
        url = reverse('meal-plans-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class CustomerAPITestCase(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Alice",
            last_name="Wonderland",
            email="alice@example.com",
            phone_number="0711111111",
            password="hash"
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
            "password": "hash"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Customer.objects.filter(email="bob@example.com").exists())

    def test_customer_unique_email(self):
        data = {
            "first_name": "Charlie",
            "last_name": "Chaplin",
            "email": "alice@example.com",  
            "phone_number": "0733333333",
            "password": "hash"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class MamaMbogaAPITestCase(APITestCase):
    def setUp(self):
        self.mama = MamaMboga.objects.create(
            kiosk_name="Mama's Place",
            first_name="Mama",
            last_name="Mboga",
            email="mama@mboga.com",
            phone_number="0744444444",
            password="hash"
        )
        self.list_url = reverse('mama-mbogas-list')

    def test_mama_mboga_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), MamaMboga.objects.count())

    def test_mama_mboga_create(self):
        data = {
            "kiosk_name": "New Kiosk",
            "first_name": "New",
            "last_name": "Owner",
            "email": "new@kiosk.com",
            "phone_number": "0755555555",
            "password": "hash"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mama_mboga_unique_email(self):
        data = {
            "kiosk_name": "Another",
            "first_name": "Dup",
            "last_name": "Owner",
            "email": "mama@mboga.com", 
            "phone_number": "0756666666",
            "password": "hash"
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
            password="hash"
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

