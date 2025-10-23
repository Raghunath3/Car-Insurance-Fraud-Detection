# fraudapp/urls.py
 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict_api, name='predict_api'),
    path('contact/', views.submit_contact, name='contact'),
]



