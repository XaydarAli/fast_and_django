from django.urls import path
from .views import HomePageView,RegisterPageView,LoginPageView,PostPageView,UsersPageView
urlpatterns = [

    path('',HomePageView.as_view(),name='home'),
    path('register/',RegisterPageView.as_view(),name='register'),
    path('login/',LoginPageView.as_view(),name='login'),
    path('posts/',PostPageView.as_view(),name='posts'),
    path('users/',UsersPageView.as_view(),name='users'),


]