from django.urls import path
from .import views

urlpatterns = [
    path('admindashboard',views.adminDashboard,name="adminDashbaord"),
    path('members',views.getMembers,name="members"),
    path('addmember',views.addMember,name="addmember"),
    path('editMmember',views.editMember,name="editMmember"),
    path('deleteMmember',views.deleteMember,name="deleteMember")
 
]


