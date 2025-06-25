from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Customer
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