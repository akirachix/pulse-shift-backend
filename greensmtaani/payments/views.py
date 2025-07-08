from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import base64
from datetime import datetime
import json

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Received callback:", data)  
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

def get_access_token():
    url = f"{settings.DARJA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(settings.DARJA_CONSUMER_KEY, settings.DARJA_CONSUMER_SECRET))
    response.raise_for_status() 
    return response.json()['access_token']

@csrf_exempt
def initiate_stk_push(request):
    print(f"###################3{request}%%%%%%%%%%")
    if request.method != 'POST':
        return JsonResponse({"error": "POST method required"}, status=400)
    phone = request.POST.get('phone')
    amount = request.POST.get('amount')
    if not phone or not amount:
        return JsonResponse({"error": "Phone and amount are required"}, status=400)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = settings.DARJA_SHORTCODE + settings.DARJA_PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode()
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": settings.DARJA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": settings.DARJA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": settings.DARJA_CALLBACK_URL,
        "AccountReference": "TestPayment",
        "TransactionDesc": "Testing STK push"
    }
    response = requests.post(
        f"{settings.DARJA_BASE_URL}/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )
    return JsonResponse(response.json())
