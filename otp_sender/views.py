from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from datetime import datetime
from pytz import timezone
from suprsend import Suprsend
from suprsend import Workflow
import random 
import string
from django.http import HttpResponseServerError
# from suprsend import create_workflow



# Import the Suprsend API library or module here

supr_client = Suprsend("BOIO4JhU8L5J1QmMa8JX", "tnncextEVjlhCP9yQzJO")

distinct_id = "arjit_goyal"  # Unique identifier of user in your application
# Instantiate User profile
user = supr_client.user.get_instance(distinct_id=distinct_id)

#Creating Workflow
workflow_body = {
  "name": "workflow_name",
  "template": "template_slug",
  "notification_category": "Transactional", # notification category transactional/promotional/system
  "delay": "time_delay",  # time delay after which the first notification will be sent
  "trigger_at": "date string in ISO 8601", #to trigger scheduled notifications

  "users": [
    {
      "distinct_id": "distinct_id", # unique identifier of the user
      # if $channels is present, communication will be triggered on mentioned channels only.
      # "$channels": ["email"],

      # User communication channel can be added as [optional]:
      # "$email":["user@example.com"],
      # "$whatsapp":["+15555555555"],
      # "$sms":["+15555555555"],
      # "$androidpush": [{"token": "__android_push_token__", "provider": "fcm", "device_id": ""}],  
      # "$iospush":[{"token": "__ios_push_token__", "provider": "apns", "device_id": ""}],
      # "$slack": {
      #  "email": "user@example.com",
      #  "access_token": "xoxb-XXXXXXXX"
      #}   --- slack using email

      # "$slack": {
      #  "user_id": "U/WXXXXXXXX",
      #  "access_token": "xoxb-XXXXXX"
      #} --- slack using member_id

      # "$slack": {
      #  "channel": "CXXXXXXXX",
      #  "access_token": "xoxb-XXXXXX"
      #} --- slack channel

      # "$slack": {
      #  "incoming_webhook": {
      #  "url": "https://hooks.slack.com/services/TXXXXXXXXX/BXXXXXXXX/XXXXXXXXXXXXXXXXXXX"
      # }
      #} --- slack incoming webhook
    }
  ],

  # delivery instruction [optional]. how should notifications be sent, and whats the success metric
#   "delivery": {
#     "smart": <boolean_value>,
#     "success": "success_metric",
#     "time_to_live": "TTL duration", # will be applicable for smart = TRUE
#     "mandatory_channels": [] # list of mandatory channels e.g ["email"], will be applicable for smart = TRUE
#   },
  # data can be any json / serializable python-dictionary
  "data": {
    "key":"value",
    "nested_key": {
      "nested_key1": "some_value_1",
      "nested_key2": {
        "nested_key3": "some_value_3",
      },
    }
  }
}   
wf = Workflow(body=workflow_body)
# Trigger workflow
response = supr_client.trigger_workflow(wf)



def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp(phone, otp):
    user.add_email("arjitgoyal1704@gmail.com") # - To add Email

    user.add_sms("+916398198242") # - To add SMS

user.set_preferred_language("en")

def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        otp = generate_otp()
        user = Users(name=name, email=email, phone=phone, otp=otp)
        user.save()
        send_otp(phone, otp)  # Send the OTP to the provided phone number

        workflow_body = {
            "distinct_id": user.distinct_id,
            "trigger_at": datetime.now(),  # Add the desired trigger time here in ISO 8601 format
            "properties": {   # Add any additional properties you want to include in the workflow
                "name": name,
                "email": email,
                "phone": phone,
                "otp": otp
            }
        }


        return redirect('verify_otp')
    return render(request, 'form.html')

# @csrf_exempt
# def verify_otp(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         phone = request.POST.get('phone')
#         user = Users.objects.get(phone=phone, otp=otp)
#         if user:
#             # OTP verification successful
#             return redirect('success')
#         else:
#             # OTP verification failed
#             return redirect('success')
#     return render(request, 'verify_otp.html')


@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        phone = request.POST.get('phone')
        try:
            user = Users.objects.get(phone=phone)
            if entered_otp == user.otp:
                # OTP verification successful
                return redirect('success')
            else:
                # OTP verification failed
                error = 'Incorrect OTP'
        except Users.DoesNotExist:
            # OTP verification failed
            error = 'OTP verification failed'

        return render(request, 'verify_otp.html', {'error': error, 'phone': phone})

    return render(request, 'verify_otp.html')


@csrf_exempt
def success(request):
    return render(request, 'success.html')
