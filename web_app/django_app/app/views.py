from django.shortcuts import render,redirect
from django.views import View
from .forms import RegisterForm,LoginForm
import requests
from django.http import HttpResponse, HttpResponseRedirect


class HomePageView(View):
    def get(self,request):
        access_token = request.COOKIES['access_token']
        if not access_token:
            return redirect('login')
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('http://127.0.0.2:8002/auth/token/verify', headers=headers)
        if response.json()['status_code'] == '200':
            return render(request, 'home.html')

        elif response.json()['status_code'] == '401':
            response=HttpResponseRedirect('/login/')
            response.delete_cookie('access_token')
            return response

        else:
            return HttpResponse("Request Failed")

        return render(request,'home.html')

class PostPageView(View):
    def get(self, request):
        access_token = request.COOKIES['access_token']
        if not access_token:
            return redirect('login')
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('http://127.0.0.2:8002/auth/token/verify', headers=headers)
        if response.json()['status_code'] == '200':
            posts=requests.get('http://127.0.0.2:8002/posts/', headers=headers)
            return render(request, 'posts.html', {'posts':posts})

        elif response.json()['status_code'] == '401':
            response = HttpResponseRedirect('/login/')
            response.delete_cookie('access_token')
            return response

        else:
            return HttpResponse("Request Failed")

        return render(request, 'posts.html')


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
                access_token = response.json()['access_token']
                response=redirect("home")
                response.set_cookie('access_token',access_token,httponly=True)

            else:
                return HttpResponse(f"Error:{response.json()['detail']}")

        else:
            return HttpResponse("Form is not valid")





class UsersPageView(View):
    def get(self,request):
        access_token = request.COOKIES['access_token']
        if not access_token:
            return redirect('login')
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get('http://127.0.0.2:8002/auth/token/verify', headers=headers)
        if response.json()['status_code'] == '200':
            users=requests.get(f'http://127.0.0.2:8002/auth/users', headers=headers)
            return render(request, 'users.html',{'users':users})

        elif response.json()['status_code'] == '401':
            response = HttpResponseRedirect('/login/')
            response.delete_cookie('access_token')
            return response

        else:
            return HttpResponse("Request Failed")

        return render(request, 'home.html')
