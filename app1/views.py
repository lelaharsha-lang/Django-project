
from django.shortcuts import render
from django.http import HttpResponse
from app1.models import User
def about(request):
    users = User.objects.all()
    i = User.objects.count()
    return render(request,'app1/about.html',{'users':users,'i':i})
def add(request):
    a = int(request.POST['num1'])
    b = int(request.POST['num2'])
    c = a + b
    return render(request,'app1/result.html',{'result':c,'num1':a,'num2':b})
def loginn(request):
    password = request.POST.get('password')

    user = User.objects.create(
    username=username,
    first_name=firstname,
    last_name=lastname,
    email=email,
    mobile_number=mobile,
    image=image,
)

    user.set_password(password)
    user.save()

def button(request):
    return render(request,'app1/button.html')

def page(request):
    return render(request,'app1/page.html')