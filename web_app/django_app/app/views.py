from django.shortcuts import render
from django.views import View
from .forms import RegisterForm,LoginForm
import requests
from django.http import HttpResponse
class HomePageView(View):
    def get(self,request):
        return render(request,'home.html')

class PostPageView(View):
    def get(self,request):
        return render(request,'posts.html')

class RegisterPageView(View):
    def get(self,request):
        form = RegisterForm()
        return render(request,'register.html',{'form':form})

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']

            url="http://127.0.0.2:8002/auth/register/"

            data={
                'username':username,
                'password':password,
                'email':email
            }
            response = requests.post(url,json=data)
            print(response.json())
            if response.json()['status_code'] == 201:
                return HttpResponse('You have successfully registered')
            else:
                return HttpResponse(f"Error:{response.json()['detail']}")
        else:
            return HttpResponse("Form is not valid")


class LoginPageView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,'login.html',{'form':form})

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            url="http://127.0.0.2:8002/auth/login/"
            data={
                "username_or_email":form.cleaned_data['username_or_email'],
                "password":form.cleaned_data['password']
            }
            response = requests.post(url,json=data)
            if response.json()['status_code'] == 200:
                return HttpResponse("You have successfully logged in")
            else:
                return HttpResponse(f"Error:{response.json()['detail']}")

        else:
            return HttpResponse("Form is not valid")


