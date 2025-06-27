
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