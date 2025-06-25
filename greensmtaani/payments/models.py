from django.db import models
from decimal import Decimal

from orders.models import Orders
from users.models import Customer


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Orders,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.RESTRICT,
        related_name='transactions'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    currency = models.CharField(
        max_length=10,
        default='KES'
    )
    payment_method = models.CharField(
        max_length=50
    )
    gateway_transaction_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
 
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES
    )
    transaction_date = models.DateTimeField(
        auto_now_add=True
    )
    response_code = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    response_message = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gt=Decimal('0.00')),
                name='amount_gt_0'
            ),
        ]

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
