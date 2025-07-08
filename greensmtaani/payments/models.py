from django.db import models
from users.models import Customer, MamaMboga
from orders.models import Orders

class Payment(models.Model):

    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='payments')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    phone_number = models.CharField(max_length=20, help_text="Payer's phone number (M-Pesa)")
    mpesa_receipt_number = models.CharField(max_length=100, null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    checkout_request_id = models.CharField(max_length=100, null=True, blank=True)
    merchant_request_id = models.CharField(max_length=100, null=True, blank=True)
    raw_callback = models.JSONField(null=True, blank=True, help_text="Raw Daraja API callback response")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_id} - {self.status}"

class Payout(models.Model):

    PAYOUT_STATUS = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]
    payout_id = models.AutoField(primary_key=True)
    mama_mboga = models.ForeignKey(MamaMboga, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYOUT_STATUS, default='PENDING')
    payout_method = models.CharField(max_length=30, default='MPESA', help_text="e.g. MPESA, Bank, Cash")
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    payout_reference = models.CharField(max_length=100, null=True, blank=True)
    payout_for_orders = models.ManyToManyField(Orders, blank=True, help_text="Orders included in this payout")
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Payout {self.payout_id} to {self.mama_mboga.kiosk_name} - {self.status}"