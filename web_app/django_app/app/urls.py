from django.urls import path
from .views import HomePageView,RegisterPageView,LoginPageView,PostPageView
urlpatterns = [

    path('',HomePageView.as_view(),name='home'),
    path('register/',RegisterPageView.as_view(),name='register'),
    path('login/',LoginPageView.as_view(),name='login'),
    path('posts/',PostPageView.as_view(),name='posts'),


]