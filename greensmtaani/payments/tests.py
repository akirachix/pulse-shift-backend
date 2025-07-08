from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from users.models import Customer, MamaMboga
from orders.models import Orders
from .models import Payment, Payout

class PaymentModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John", last_name="Doe", phone_number="0712345678"
        )
        self.order = Orders.objects.create(
            customer=self.customer,
            total_amount=Decimal("500.00"),
            order_preference_fee=Decimal("0.00"),
            current_status="PENDING",
            payment_status="PENDING"
        )

    def test_create_payment_with_minimum_fields(self):
        payment = Payment.objects.create(
            order=self.order,
            customer=self.customer,
            total_amount=Decimal("100.00"),  # <-- USE total_amount
            phone_number="0712345678"
        )
        self.assertEqual(payment.status, 'PENDING')
        self.assertIsNone(payment.mpesa_receipt_number)
        self.assertIsNone(payment.transaction_date)
        self.assertIsNone(payment.checkout_request_id)
        self.assertIsNone(payment.merchant_request_id)
        self.assertIsNone(payment.raw_callback)
        self.assertIsNotNone(payment.created_at)
        self.assertIsNotNone(payment.updated_at)
        self.assertEqual(str(payment), f"Payment {payment.payment_id} for Order {self.order.order_id} - {payment.status}")

    def test_payment_status_choices(self):
        payment = Payment.objects.create(
            order=self.order, customer=self.customer, total_amount=Decimal("100.00"), phone_number="0712345678"
        )
        for status, _ in Payment.PAYMENT_STATUS:
            payment.status = status
            payment.save()
            self.assertEqual(payment.status, status)

    def test_update_payment_fields(self):
        payment = Payment.objects.create(
            order=self.order, customer=self.customer, total_amount=Decimal("100.00"), phone_number="0712345678"
        )
        payment.status = 'SUCCESS'
        payment.mpesa_receipt_number = "MPESA12345"
        now = timezone.now()
        payment.transaction_date = now
        payment.save()
        updated = Payment.objects.get(pk=payment.pk)
        self.assertEqual(updated.status, 'SUCCESS')
        self.assertEqual(updated.mpesa_receipt_number, "MPESA12345")
        self.assertEqual(updated.transaction_date, now)

    def test_delete_order_cascades_payment(self):
        payment = Payment.objects.create(
            order=self.order, customer=self.customer, total_amount=Decimal("100.00"), phone_number="0712345678"
        )
        self.order.delete()
        self.assertEqual(Payment.objects.count(), 0)

class PayoutModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Jane", last_name="Doe", phone_number="0712345679"
        )
        self.mama_mboga = MamaMboga.objects.create(
            kiosk_name="Mama's Veggies", phone_number="0712345670"
        )
        self.order1 = Orders.objects.create(
            customer=self.customer,
            total_amount=Decimal("200.00"),
            order_preference_fee=Decimal("0.00"),
            current_status="PENDING",
            payment_status="PENDING"
        )
        self.order2 = Orders.objects.create(
            customer=self.customer,
            total_amount=Decimal("300.00"),
            order_preference_fee=Decimal("0.00"),
            current_status="PENDING",
            payment_status="PENDING"
        )

    def test_create_payout_with_minimum_fields(self):
        payout = Payout.objects.create(
            mama_mboga=self.mama_mboga,
            amount=Decimal("300.00")
        )
        self.assertEqual(payout.status, 'PENDING')
        self.assertEqual(payout.payout_method, 'MPESA')
        self.assertIsNone(payout.transaction_id)
        self.assertIsNone(payout.payout_reference)
        self.assertIsNone(payout.processed_at)
        self.assertIsNone(payout.notes)
        self.assertIsNotNone(payout.created_at)
        self.assertEqual(str(payout), f"Payout {payout.payout_id} to {self.mama_mboga.kiosk_name} - {payout.status}")

    def test_payout_status_choices(self):
        payout = Payout.objects.create(mama_mboga=self.mama_mboga, amount=Decimal("200.00"))
        for status, _ in Payout.PAYOUT_STATUS:
            payout.status = status
            payout.save()
            self.assertEqual(payout.status, status)

    def test_payout_many_to_many_orders(self):
        payout = Payout.objects.create(mama_mboga=self.mama_mboga, amount=Decimal("400.00"))
        payout.payout_for_orders.add(self.order1, self.order2)
        self.assertIn(self.order1, payout.payout_for_orders.all())
        self.assertIn(self.order2, payout.payout_for_orders.all())
        self.assertEqual(payout.payout_for_orders.count(), 2)

    def test_update_and_delete_payout(self):
        payout = Payout.objects.create(mama_mboga=self.mama_mboga, amount=Decimal("500.00"))
        payout.status = "SUCCESS"
        payout.notes = "Test payout"
        payout.save()
        updated = Payout.objects.get(pk=payout.pk)
        self.assertEqual(updated.status, "SUCCESS")
        self.assertEqual(updated.notes, "Test payout")
        payout.delete()
        self.assertEqual(Payout.objects.count(), 0)

    def test_delete_mama_mboga_cascades_payout(self):
        payout = Payout.objects.create(mama_mboga=self.mama_mboga, amount=Decimal("300.00"))
        self.mama_mboga.delete()
        self.assertEqual(Payout.objects.count(), 0)