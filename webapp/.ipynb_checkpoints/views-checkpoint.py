from django.shortcuts import render

def myapp(request):
    return render(request, 'temp/login.html')

def signup(request):
    return render(request, 'temp/signup.html')

def forget(request):
    return render(request, 'temp/forget.html')

def verify(request):
    return render(request, 'temp/verify.html')

def update(request):
    return render(request, 'temp/update_pass.html')