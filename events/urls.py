from django.urls import path
from .import views


urlpatterns = [
   path('events',views.getEvents,name='events'),
   path('addEvent',views.addEvent,name="addEvent"),
   path('deleteEvent',views.delete_event,name="deleteEvent"),
   path('updateEvent',views.updateEvent,name='updateEvent')
   
]
