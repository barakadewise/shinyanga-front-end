from django.urls import path
from .import views


urlpatterns = [
 path('members',views.viewMember,name="members"),
 path('viewEvents',views.viewEvents,name="viewEvents"),
 path('memberdonation',views.getDonations,name='memeberdonation'),
 path('memberDashboard',views.memberDashboard,name="memberDashboard")
   
]


