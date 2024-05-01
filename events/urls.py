from django.urls import path
from .import views


urlpatterns = [
   path('events',views.getEvents,name='events'),
   path('editEvent',views.editEvent,name="editEvent"),
   path('addEvent',views.addEvent,name="addEvent")
   
]


