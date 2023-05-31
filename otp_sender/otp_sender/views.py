from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import User


def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        user = User(name=name, email=email, phone=phone)
        user.save()
        return redirect('success')
    return render(request, 'form.html')

@csrf_exempt
def success(request):
    return render(request, 'success.html')