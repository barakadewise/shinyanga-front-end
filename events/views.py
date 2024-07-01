from django.shortcuts import render,redirect

from django.http import JsonResponse
from django.contrib import messages

from api.api import ApiService

# Create your views here.
api =ApiService()


def getEvents(request):
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
    
 
    
   #check if edit post is sent 
    if request.method=='POST':
        id =float(request.POST.get('id'))
        agenda=request.POST.get('agenda')
        coverage=request.POST.get('coverage')
        startDate =request.POST.get('startDate')
        endDate =request.POST.get('endDate')

        mutation = '''
           mutation UpdateEvent($input: UpdateEventInput!, $eventId: Float!) {
           updateEvent(updateEventInput: $input, eventId: $eventId) {
            message
             statusCode
            }
           }

        '''
        variables = {
            'input': {
                'agenda': agenda,
                'coverage': coverage,
                'startDate': startDate,
                'endDate': endDate
            }
            ,
            'eventId':id
        }
       
        eventEdit = api.performMuttion(mutation,variables)
        if 'errors' in eventEdit:
            print(eventEdit['errors'])
            messages.error(request,eventEdit['error'][0])
        else:
            messages.success(request,"Updated Successfully!")    

     # pull data  from the api 
    response = api.performQuery(query,api.getCsrfToken(request))
    if 'errors' in response:
        print(response,"Eroors")
        return render(request, 'events.htm')
    if 'data' in response:
        events = response.get('data', {}).get('findAllEvents', [])
        print(events)
        return render(request, 'events.html', {'events': events})
    else:
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


# def editEvent(request):
#     if request.method=="POST":
#         print("Request to edit event made!")
#         messages.info(request,'Edit eent started')
       
def delete_event(request):
    if request.method=="POST":
      
        id =float(request.POST.get('id'))
        print(id)
        muatation='''
        mutation($id: Float!) {
            removeEvent(id:$id){
             message,
             statusCode
           }
         }
  
        '''
        response = api.performMuttion(muatation,{'id':id} )
        if 'errors' in response:
            messages.error(request,'Failed to delete User!')
            print(response['errors'])
            return redirect('events')
          
        else:
            messages.success(request,response['data'][' removeEvent']['message'])
            return redirect('events')
        
        
      
def updateEvent(request):
        if  request.method =="POST":
            agenda=request.POST.get('agenda')
            coverage=request.POST.get('coverage')
            startDate =request.POST.get('startDate')
            endDate =request.POST.get('endDate')

            print(agenda,startDate,endDate,coverage)