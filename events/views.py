from django.shortcuts import render,redirect

from django.http import JsonResponse
from django.contrib import messages

from api.api import ApiService

# Create your views here.
api =ApiService()


def getEvents(request):
    # Define your GraphQL query
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
    
 
    
    # Make the GraphQL request
    response = api.performQuery(query,api.getCsrfToken(request))

    if 'errors' in response:
        print(response,"Eroors")
        return response
    if 'data' in response:
        events = response.get('data', {}).get('findAllEvents', [])
        print(events)
        return render(request, 'events.html', {'events': events})
    else:
        
        print(response)
        return render(request, 'events.htm')




def addEvent(request):
    if request.method == 'POST':
        agenda = request.POST.get('agenda')
        coverage = request.POST.get('coverage')
        location = request.POST.get('location')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')

        
    
        mutation = '''
            mutation CreateEvent($input: CreateEventInput!) {
              createEvent(createEventInput: $input) {
                id
                agenda
                location
              }
            }
        '''
        variables = {
            'input': {
                'agenda': agenda,
                'coverage': coverage,
                'location': location,
                'startDate': startDate,
                'endDate': endDate
            }
        }
       
        
        # Make the GraphQL request
        response = api.performMuttion(mutation,variables)
        
        if 'errors' in response:
            print("response has got errors:",response)
            if response['errors'][0]['statusCode']==401:
                messages.error(request,'Failed to add event!')
              
            else:
               messages.error(request,response['errors'][0]['message'])
            
        elif 'data' in response:
            print("response data",response)
            messages.success(request,'Successfully added Event')
            return redirect('events')

        else:
            messages.error(request,'Failed due to Network issues')
    return render(request, 'addEvent.html')


def editEvent(request):
    return render(request,'editEvent.html')