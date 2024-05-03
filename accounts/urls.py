from django.urls import path
from .import views


urlpatterns = [
   path('',views.signupPage,name='signup'),
   path('complete-profile/<int:account_id>/',views.completeProfile,name="complete-profile"),
   path('login',views.loginPage,name='login')
   
]


