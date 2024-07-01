from django.shortcuts import render,redirect
from django.contrib import messages
from api.api import ApiService

api = ApiService()
#member dashboard
def memberDashboard(request):
  
    query ='''
        query {
        getUserProfile {
        name
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
        print("profile:",response)
        return render(request,'member-dash.html')


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
        return render(request, 'view_events.html', {'events': response.get('data', {}).get('findAllEvents', [])})
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



#get user profile name 
def getUserName(request):
    query ='''
        query {
        getUserProfile {
        name
        }
       }
    '''
    token=request.session.get('token')
    response = api.performQueryWithToken(query,api.getCsrfToken(request),token)
    if 'errors' in response:
        print(response['errors'])
        messages.error(request,response['errors'][0]['message'])
        print(response)
        request.session.clear()
        return redirect('login')
    else:
        print("profile:",response)
        return {'profile':response['data']['getUserProfile']}
    


