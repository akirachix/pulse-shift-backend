

from django.test import TestCase
from django.test import TestCase
from django.utils import timezone
from users.models import Customer
from .models import DietaryPreference, MealPlan
import datetime

class DietaryPreferenceModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        phone_number="0712345678",
        password="supersecret"
)
        
     

    def test_create_dietary_preference(self):
        pref = DietaryPreference.objects.create(
            customer=self.customer,
            dietary_type="Vegan",
            excluded_ingredients=["peanuts", "gluten"],
            favorite_cuisines=["Italian", "Indian"],
            preferred_meal_types=["breakfast", "dinner"],
            nutritional_goal="High Protein"
        )
        self.assertEqual(pref.customer, self.customer)
        self.assertEqual(pref.dietary_type, "Vegan")
        self.assertListEqual(pref.excluded_ingredients, ["peanuts", "gluten"])
        self.assertListEqual(pref.favorite_cuisines, ["Italian", "Indian"])
        self.assertListEqual(pref.preferred_meal_types, ["breakfast", "dinner"])
        self.assertEqual(pref.nutritional_goal, "High Protein")
        self.assertIsNotNone(pref.created_at)
        self.assertIn("Vegan", str(pref))

    def test_blank_array_fields(self):
        pref = DietaryPreference.objects.create(
            customer=self.customer,
            dietary_type="Vegetarian",
            nutritional_goal="Balanced"
        )
        self.assertEqual(pref.excluded_ingredients, [])
        self.assertEqual(pref.favorite_cuisines, [])
        self.assertEqual(pref.preferred_meal_types, [])

class MealPlanModelTest(TestCase):
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

    def test_create_meal_plan(self):
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=7)
        plan = MealPlan.objects.create(
            customer=self.customer,
            name="Weekly Keto Plan",
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            base_preference=self.preference,
            version=1
        )
        self.assertEqual(plan.customer, self.customer)
        self.assertEqual(plan.name, "Weekly Keto Plan")
        self.assertEqual(plan.start_date, start_date)
        self.assertEqual(plan.end_date, end_date)
        self.assertTrue(plan.is_active)
        self.assertEqual(plan.base_preference, self.preference)
        self.assertEqual(plan.version, 1)
        self.assertIsNotNone(plan.created_at)
        self.assertIn("Weekly Keto Plan", str(plan))

    def test_meal_plan_without_preference(self):
        start_date = datetime.date.today()
        end_date = start_date + datetime.timedelta(days=3)
        plan = MealPlan.objects.create(
            customer=self.customer,
            name="Short Plan",
            start_date=start_date,
            end_date=end_date
        )
        self.assertIsNone(plan.base_preference)
        self.assertTrue(plan.is_active)
        self.assertEqual(plan.version, 1)

   


