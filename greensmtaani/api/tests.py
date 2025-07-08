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
        first_name="John", last_name="Doe", phone_number="0712345678"
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