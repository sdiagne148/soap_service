# mysoapapp/urls.py
from django.urls import path
from mysoapapp.views import  my_soap_application

urlpatterns = [
    path('soap_service/', my_soap_application),
]
