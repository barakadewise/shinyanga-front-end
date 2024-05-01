from django.shortcuts import render
from django.http import JsonResponse
from api.api import ApiService
from utils.enum import Status
from django.contrib import messages
import json

#Api instance 
api =ApiService()


def adminDashboard(request):
    query_users = '''
    query {
      findAllUsers {
        id
      }
    }
    '''
    query_events = '''
    query {
      findAllEvents {
        id
      }
    }
    '''


    # Make requests to GraphQL server
    response_users = api.performQuery(query_users,api.getCsrfToken(request))
    response_events = api.performQuery(query_events,api.getCsrfToken(request))

    # Parse GraphQL responses
    total_users = len(response_users['data']['findAllUsers'])
    total_events = len(response_events['data']['findAllEvents'])

    # Pass data to the template
    context = {
        'total_users': total_users,
        'total_events': total_events,
    }
    print(context)
    return render(request, 'dashboard.html', context)



def getMembers(request):
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
      }
    }
    '''


  response_users = api.performQuery(query_users,api.getCsrfToken(request))
  print(response_users)
  users = response_users['data']['findAllUsers']

  context = {
        'users': users,
    }
  return render(request,'members.html',context)


def addMember(request):
    if request.method == "POST":
        # Extracting form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        region = request.POST.get('Region')
        district = request.POST.get('district')
        ward = request.POST.get('Ward')
        role = request.POST.get('role')
        status = request.POST.get('status')

        # Account creation mutation
        accountMutation = '''
          mutation($email: String!, $password: String!, $role: String!) {
            createAccount(
              createAccountInput: { email: $email, password: $password, role: $role }
            ) {
              id
              email
              role
            }
          }
        '''
        accountVariables = {
            "email": email,
            "password": password,
            "role": role 
        }

        if password == confirm_password:
            if role != "Role" and status != "Status":
                try:
                    # Perform account creation mutation
                    account_response = api.performMuttion(accountMutation, accountVariables)
                    
                    # Check if there are errors in the response
                    if 'errors' in account_response:
                        error_message = account_response['errors'][0]['message']
                        messages.error(request,error_message)
                        print(error_message)
                       

                    # If there are no errors, continue with member creation
                    if 'data' in account_response and 'createAccount' in account_response['data']:
                        account_id = account_response['data']['createAccount']['id']

                        # Member creation mutation
                        memberMutation = '''
                          mutation ($name: String!, $region: String!, $ward: String!, $phone: String!, $accountId: Float!) {
                            createUser(
                              createUserInput: {
                                name: $name,
                                region: $region,
                                ward: $ward,
                                phone: $phone,
                                accountId: $accountId
                              }
                            ) {
                              accountId
                              id
                              region
                            }
                          }
                        '''
                        memberVariables = {
                            "name": name,
                            "region": region,
                            "ward": ward,
                            "phone": phone,
                            "accountId": account_id
                        }
                        print(memberVariables)
                        # Perform member creation mutation
                        member_response = api.performMuttion(memberMutation, memberVariables)
                        if member_response:
                            print("Member created successfully.")
                            messages.success(request,"Member created successfully.")
                         
                        else:
                            print("Error creating member.")
                            messages.error(request,"Error creating member")
                         
                except Exception as e:
                    print("An error occurred:")
                    messages.error(request,"An error occurred:", str(e))
                  
            else:
                print("Role or status is not correct.")
                messages.error(request,"Role or status is not correct.")
              
        else:
            print('Password mismatch error.')
            messages.error(request,"Password mismatch error.")

    return render(request, 'add_member.html')


def getTestpage(request):
    return render(request,'test.html')