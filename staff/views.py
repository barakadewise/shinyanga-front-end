from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from api.api import ApiService
from dateutil import parser
from django.contrib import messages


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
    queryP ='''
      query {
        getStaffProfile {
           fname
           id
         }
       }
      '''

    token = request.session.get('token')
    
    profile_respone=api.performQueryWithToken(queryP,api.getCsrfToken(request),token)

    if 'errors' in profile_respone:
        print(profile_respone['errors'])
        messages.error(request,profile_respone['errors'][0]['message'])
        request.session.clear()
        return redirect('login')
    else:
     
        print("profile:",profile_respone['data']['getStaffProfile'])
        response_users = api.performQuery(query_users,api.getCsrfToken(request))
        response_events = api.performQuery(query_events,api.getCsrfToken(request))
        total_users = len(response_users['data']['findAllUsers'])
        total_events = len(response_events['data']['findAllEvents'])

       # Pass data to the template
        context = {
        'total_users': total_users,
        'total_events': total_events,
        'profile':profile_respone['data']['getStaffProfile']['fname'],
        }
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
  return render(request,'members.html',context)


def getAllUsers(request):
    #grapghql endpoint 
    query ='''
       query{
        findAllAccounts{
          id
          email
          role
           }
       }
    '''
    respone =api.performQuery(query,api.getCsrfToken(request))
    if 'errors' in respone:
        print("======ERRRO======\n",respone)
        return HttpResponse(messages.error(request,"Something went Wrong!"))

    context={
        'accounts':respone['data']['findAllAccounts']
    }
    return render(request,"allusers.html",context)

def deleteAccount(request):
    mutation ='''
         mutation($ID:Float!) {
          deleteAccount(accountId: $ID) {
           message
            statusCode
             }
           }
     '''
    
    if request.method =="POST":
        accountId= request.POST.get('id')
        response= api.performMuttion(mutation,{"ID":int(accountId)})
        if 'errors' in response:
             return HttpResponse(messages.error(request,response['errors'][0]['message']))
        print(response)
        return HttpResponse(messages.success(request,"Account Sussccessfully deleted!"))
            

def addMember(request):
    if request.method == "POST":
      
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        region = request.POST.get('Region')
        profession=request.POST.get('profession')
        ward = request.POST.get('Ward')
        role = request.POST.get('role')
      

        # Account creation mutation
        accountMutation = '''
          mutation($email: String!, $password: String!, $role: String!) {
            createStaffOrMemberAccount(
              createStaffOrMemberInput: { email: $email, password: $password, role: $role }
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
            if role != "Role":
                try:
                    # Perform account creation mutation
                    account_response = api.performMuttion(accountMutation, accountVariables)
                    
                    # Check if there are errors in the response
                    if 'errors' in account_response:
                        error_message = account_response['errors'][0]['message']
                        messages.error(request,error_message)
                      
                       

                    # If there are no errors, continue with member creation
                    if 'data' in account_response and 'createStaffOrMemberAccount' in account_response['data']:
                        account_id = account_response['data']['createStaffOrMemberAccount']['id']

                        # Member creation mutation
                        memberMutation = '''
                          mutation ($name: String!, $region: String!, $ward: String!, $phone: String!,$profession: String!, $accountId: Float!) {
                            createUser(
                              createUserInput: {
                                name: $name,
                                region: $region,
                                ward: $ward,
                                phone: $phone,
                                profession:$profession,
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
                            "accountId": account_id,
                            "profession":profession
                        }
                        
                        if account_response['data']['createStaffOrMemberAccount']['role']=='Member':
                            member_response = api.performMuttion(memberMutation, memberVariables)
                            if 'data' in member_response:
                                print('Member created successfuly',member_response)
                                messages.success(request,"Member created successfully.")
                                return redirect('viewMembers')
                            
                            elif 'errors' in member_response: 
                                print("Error creating member.",member_response)
                                messages.error(request,"Error creating member") 
                                return redirect('addmember')
            
                except Exception as e:
                    print("An error occurred:")
                    messages.error(request,"An error occurred:", str(e))
                    return redirect('addmember')
                  
            else:
               
                messages.error(request,"Role is  not  correct.")
                return redirect('addmember')
              
        else:
            print('Password mismatch error.')
            messages.error(request,"Password mismatch error.")
            return redirect('addmember')

    return render(request, 'add_member.html')



def editMember(request):
    if request.method == 'POST':
        userId = request.POST.get('id')
        name = request.POST.get('editName')
        phone = request.POST.get('editPhone')
        profession = request.POST.get('editProfession')
        ward = request.POST.get('editWard')
        region = request.POST.get('editRegion')
        status = request.POST.get('editStatus')

        print(userId,name,phone,profession,ward)
        mutation = """
        mutation UpdateUser($input: UpdateUserInput!,$userId:Float!) {
          updateUser(updateUserInput: $input,userId:$userId) {
            statusCode
            message
          }
        }
        """

        
        variables = {
            'input': {
                'name': name,
                'phone': phone,
                'profession': profession,
                'ward': ward,
                'region': region,
                'status': status,
            },
             'userId': int(userId),
        }

        try:
            
            response = api.performMuttion(mutation,variables)
            if 'errors' in response:
                print(response['errors'])
                messages.error(request,"Faiiled to Update Member.")
                return JsonResponse({status:400})
            
            messages.success(request,"Successfully Updated Member.")
            return JsonResponse({status:200})
        
        except Exception as e:
            print("Unkonwn exception occured:",e)
            return redirect('members')
           
           

def deleteMember(request):
    mutation ='''
      mutation ($id:Float!){
      removeUser(id: $id) {
       message
       statusCode
      }
     }

    '''
    if request.method =="POST":
        id =request.POST.get('id')
        response=api.performMuttion(mutation,{"id":int(id)})

        if 'errors' in response:
            return HttpResponse(  messages.error(request,"Failed to delete Member"))
        
        return HttpResponse( messages.success(request,"Successfully deleted"))




def viewDonation(request):
    query = '''
        query {
          findAllEvents {
            id
            agenda
            coverage
          }
        }
    '''

    query_users = '''
        query {
          findAllUsers {
            id
            name
          }
        }
    '''
  
    queryDonations = '''
        query {
            findAllDonations {
                id
                createdAt
                donationFor
                donorName
                amount
            }
        }
    '''
  
    donationResponse = api.performQuery(queryDonations, api.getCsrfToken(request))
    donatedEventResponse = api.performQuery(query, api.getCsrfToken(request))
    userResponse = api.performQuery(query_users, api.getCsrfToken(request))
  
    # Format the donation data
    formatted_donations = []
    for donation in donationResponse['data']['findAllDonations']:
       
        created_at = donation['createdAt']
        dt = parser.isoparse(created_at)  # Use dateutil.parser to handle the ISO 8601 format
        formatted_date = dt.strftime('%Y-%m-%d')  # Format the date without time
        donation['createdAt'] = formatted_date
        formatted_donations.append(donation)
    
    context = {
        'donations': formatted_donations,
        'donatedEvents': donatedEventResponse['data']['findAllEvents'],
        'users': userResponse['data']['findAllUsers']
    }
    return render(request, "donations.html", context)


def addDonation(request):
    mutation = '''
    mutation AddNewDonation($amount: Int!, $donationFor: String!, $userId: Float!) {
      addNewDonation(
        createDonationInput: { amount: $amount, donationFor: $donationFor }
        userId: $userId
      ) {
        id
        userId
      }
    }
    '''

    if request.method == 'POST':
        # Retrieve form data
        amount = request.POST.get('amount')
        donor = request.POST.get('donor')
        donatedEvent = request.POST.get('donatedEvent')
      

        # Prepare variables for the mutation
        variables = {
            "amount": int(amount),  
            "donationFor": donatedEvent,
            "userId": int(donor),  
        }

        # Perform the mutation
        response = api.performMuttion(mutation, variables)
        
        # Check for errors in the response
        if 'errors' in response:
            print("======== ERRORS ========\n", response)
            messages.error(request, "Failed: Something went wrong")
            return redirect('viewDonations')
        
        # Success message
        messages.success(request, "Successfully added!")
        return redirect('viewDonations')

    
