from django.http import HttpResponse
import requests
from .credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'navbar': 'home'})


def token(request):
    validated_mpesa_access_token = MpesaAccessToken.get_access_token()
    return render(request, 'token.html', {"token": validated_mpesa_access_token})


def pay(request):
    if request.method == "POST":
        raw_phone = request.POST['phone'].strip().replace("+", "").replace(" ", "")
        if raw_phone.startswith("0"):
            phone = "254" + raw_phone[1:]
        elif not raw_phone.startswith("254"):
            phone = "254" + raw_phone
        else:
            phone = raw_phone

        amount = int(request.POST['amount'])
        access_token = MpesaAccessToken.get_access_token()
        password, timestamp = LipanaMpesaPpassword.generate_password()

        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Future Tech",
            "TransactionDesc": "Web Development Charges"
        }

        response = requests.post(api_url, json=payload, headers=headers)
        return HttpResponse(response.text)

    return HttpResponse("Invalid request method. Submit the form from /stk.")


def stk(request):
    return render(request, 'pay.html', {'navbar': 'stk'})
