from django.shortcuts import render

from api.api import ApiService

# Create your views here.
api =ApiService()
def homePage(request):
    #peform query for events
    context ={'events':[]}
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
    response = api.performQuery(query,api.getCsrfToken(request))
    
    for event in response['data']['findAllEvents']:
        if len(context['events'])<=4:
            context['events'].append(event)
            

        else:
            break

    print(context)
    return render(request,'index.html',context)