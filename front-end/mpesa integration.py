import json
import requests


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer w7gUzxgTPVlE9uiF9uirFhICovxP'
}

payload = {
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjIwOTMwMTg0MDI1",
    "Timestamp": "20220930184025",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254723629277,
    "PartyB": 174379,
    "PhoneNumber": 254723629277,
    "CallBackURL": "https://9374-2c0f-fe38-240a-f72-50bb-aa3-b6dd-1727.in.ngrok.io/api/payments/mpesa",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 
}
response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)

api_response = json.loads(response.text.encode('utf8'))

print(api_response)