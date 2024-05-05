from django.urls import path
from .import views


urlpatterns = [
 path('viewmembers',views.viewMember,name="viewmembers"),
 path('viewEvents',views.viewEvents,name="viewEvents"),
 path('memberDashboard/<str:token>',views.memberDashboard,name="memberDashboard")
   
]


