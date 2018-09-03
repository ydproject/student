from django.shortcuts import render

# Create your views here.


# 登录
def login(request):
    return render(request, 'login.html')