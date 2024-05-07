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
        # messages.success(request,'Successfully loggedin!')
        print("profile:",response)
        return render(request,'member-dash.html',{'profile':response['data']['getUserProfile']})


#view events
def viewEvents(request):
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
        messages.error(request,'Something went wrong')
    if 'data' in response:
        events = response.get('data', {}).get('findAllEvents', [])
        print(events)
        return render(request, 'view_events.html', {'events': events})
    else:
        print(response)
        messages.error(request,'Something went wrong')

#view members
def viewMember(request):
 query_users = '''
    query {
      findAllUsers {
        id
        name
        phone
        email
        region
        ward
        status
        profession
      }
    }
    '''
 response_users = api.performQuery(query_users,api.getCsrfToken(request))
 print(response_users)
 users = response_users['data']['findAllUsers']
 context = {
        'users': users,
    }
 return render(request,'view_member.html',context)