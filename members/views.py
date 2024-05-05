from django.shortcuts import render,redirect
from django.contrib import messages
from api.api import ApiService

api = ApiService()
#member dashboard
def memberDashboard(request,token):
    #get user profile data
    query ='''
        query {
  getUserProfile {
    region
    name
    id
  }
}
    '''
    response = api.performQueryWithToken(query,api.getCsrfToken(request),token)
    if 'errors' in response:
        print(response['errors'])
        messages.error(request,response['errors'][0]['message'])
        return redirect('signup')
    else:
        messages.success(request,'Successfully loggedin!')
        
    return render(request,'member-dash.html',)


#view events
def viewEvents(request):
    return render(request,'view_events.html')

#view members
def viewMember(request):
    return render(request,'view_member.html')