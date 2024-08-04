from django.urls import path
from .import views

urlpatterns = [
    path('admindashboard',views.adminDashboard,name="adminDashbaord"),
    path('viewmembers',views.getMembers,name="viewMembers"),
    path('addmember',views.addMember,name="addmember"),
    path('editMmember',views.editMember,name="editMmember"),
    path('deleteMmember',views.deleteMember,name="deleteMember"),
    path('allusers',views.getAllUsers,name="allusers"),
    path('deleteAccount',views.deleteAccount,name="deleteUserAccount"),
    path('veiwDonations',views.viewDonation,name='viewDonations'),
    path('addDonation',views.addDonation,name='addDonation')
 
]


