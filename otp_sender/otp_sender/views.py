from django.shortcuts import render, redirect
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

def success(request):
    return render(request, 'success.html')