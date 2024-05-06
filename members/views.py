from django.shortcuts import render,redirect
from django.contrib import messages
from api.api import ApiService

api = ApiService()
#member dashboard
def memberDashboard(request):
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
    token=request.session.get('token')
    print(token)
    response = api.performQueryWithToken(query,api.getCsrfToken(request),token)
    if 'errors' in response:
        print(response['errors'])
        messages.error(request,response['errors'][0]['message'])
        print(response)
        request.session.clear()
        return redirect('login')
    else:
        messages.success(request,'Successfully loggedin!')
        print("profile:",response)
        return render(request,'member-dash.html',{'profile':response['data']['getUserProfile']})


#view events
def viewEvents(request):
    return render(request,'view_events.html')

#view members
def viewMember(request):
    return render(request,'view_member.html')