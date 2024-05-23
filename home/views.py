from django.shortcuts import render,redirect
from django.contrib import messages
from api.api import ApiService

# Create your views here.
api =ApiService()
def homePage(request):
    context = {'events': []}
    
    query = '''
        query {
          findAllEvents {
            id
            agenda
            coverage
            startDate
            endDate
          }
        }
    '''
    
    response = api.performQuery(query, api.getCsrfToken(request))
        
    if 'data' in response and 'findAllEvents' in response['data']:
        events = response['data']['findAllEvents']
            
        context['events'] = events[:4]
    else:
        context['error'] = 'Failed to fetch events data.'
    
    return render(request, 'index.html', context)


def viewEventCard(request):
    if 'token' in request.session:
        print("Your allowed to vie this events..")
        messages.success(request,'Allowed to view!')
        return redirect('viewEvents')
    else:
        messages.error(request,'Please Login in to view events')
        print("Please loggin in to view events!")  
        return redirect('homepage')  