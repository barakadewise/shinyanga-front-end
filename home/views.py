from django.shortcuts import render

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