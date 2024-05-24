
from api.api import ApiService

def user_profile_context_processor(request):
    api_service = ApiService()
    user_name = api_service.userProfileName(request)
    return {
        'user_name': user_name
    }

