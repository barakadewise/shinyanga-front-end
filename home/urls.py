from django.urls import path
from .import views


urlpatterns = [
    path('',views.homePage,name='homepage'),
    path('viewEvent',views.viewEventCard,name='viewEvent')
  
]


