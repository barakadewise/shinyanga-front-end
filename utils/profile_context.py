
from api.api import ApiService
from django.contrib import sessions
# class UserProfileContextProcessor:
#     def __init__(self):
#         self.api_service = ApiService()

#     def fetch_user_profile(self, request):
#         user_name = self.api_service.userProfileName(request)
#         return {'user_name': user_name}

    # def fetch_staff_profile(self, request):
    #     staff_name = self.api_service.staffProfileName(request)
    #     return {'staff_name': staff_name}

    # def __call__(self, request):
    #     return self.fetch_user_profile(request)

def user_profile_context_processor(request):
    api_service = ApiService()
    user_name = api_service.userProfileName(request)
   
    return {'user_name': user_name}