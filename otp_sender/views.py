# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
# from .models import Users
# import random 
# import string

# def generate_otp(length=6):
#     return ''.join(random.choices(string.digits, k=length))

# def register_user(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         otp = generate_otp()
#         user = Users(name=name, email=email, phone=phone, otp= otp)
#         user.save()
#         return redirect('success')
#     return render(request, 'form.html')

# @csrf_exempt
# def success(request):
#     return render(request, 'success.html')








from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from suprsend import Suprsend
from suprsend import Workflow
import random 
import string

# Import the Suprsend API library or module here

supr_client = Suprsend("BOIO4JhU8L5J1QmMa8JX", "tnncextEVjlhCP9yQzJO")

distinct_id = "arjit_goyal"  # Unique identifier of user in your application
# Instantiate User profile
user = supr_client.user.get_instance(distinct_id=distinct_id)

#Creating Workflow



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
        return redirect('verify_otp')
    return render(request, 'form.html')

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        phone = request.POST.get('phone')
        user = Users.objects.get(phone=phone, otp=otp)
        if user:
            # OTP verification successful
            return redirect('success')
        else:
            # OTP verification failed
            return redirect('success')
    return render(request, 'verify_otp.html')

@csrf_exempt
def success(request):
    return render(request, 'success.html')
