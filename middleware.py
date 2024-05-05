# middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        disallowed_urls = [
            '/adminDashbaord','/editEvent',
            '/events','/addEvent','/members',
            '/addmember'
            ]

        if request.path in disallowed_urls:
            print("Accessing token ..path....")
            if 'token' in request.session:
                return self.get_response(request)
            else:
                print("No token")
                return redirect(reverse('login'))

        else:
            print("Allowed....path ")
            return self.get_response(request)
           

      


