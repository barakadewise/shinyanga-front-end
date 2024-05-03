
from django.contrib import admin
from django.urls import path,include

urlpatterns = [

    path('',include('home.urls')),
    path('', include('staff.urls')),
    path('',include('accounts.urls')),
    path('', include('events.urls')),
]
