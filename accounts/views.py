from django.shortcuts import render,redirect
import re
from django.contrib import messages
from django.http import JsonResponse
from django.contrib import sessions

from api.api import ApiService

# api instancee
api =ApiService()

#loging function 
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Define the GraphQL mutation query with variables
        mutation = '''
        mutation LoginMutation($username: String!, $password: String!) {
          login(loginUserDto: {
            username: $username,
            password: $password
          }) {
            message
            access_token
            role
          }
        }
        '''

        variables = {
            'username': email,
            'password': password
        }

        # Make a POST request to your GraphQL endpoint
        response = api.performMuttion(mutation,variables)

     
        if 'errors' in response:
            messages.error(request,response['errors'])
            print('Error:',response)
            return render(request,'login.html')

        elif 'data' in response:
           print(response)
           data =response['data']['login']
           print('Auth Results:',data)
           if data and 'access_token' in data:
               print(data['access_token'])
               messages.success(request,data['message'])
               return render(request,'login.html',{'token':data['access_token']})

        else:
            print("Something went wrong")
            messages.error(request,'Something went wrong!')
            print(response)
            return render(request,'login.html')

    return render(request, 'login.html')


#signup function
def signupPage(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        

         # Construct the GraphQL mutation
        mutation = """
            mutation CreateAccount($input: CreateAccountInput!) {
                createAccount(createAccountInput: $input) {
                    id
                    email
                    password
                }
            }
        """

        # Variables for the GraphQL mutation
        variables = {
            "input": {
                "email": email,
                "password": password1,
                
            }
        }

        if  is_valid_email(email):
            if password1==password2:
                if len(password1)>=5:
                    #create account
                    response=api.performMuttion(mutation,variables)
                    if 'errors' in response:
                        print(response['errors'])
                        messages.error(request,response['erros'][0]['message'])
                        return JsonResponse(response)
                    elif 'data' in response:
                        print("Opertion was successfully")
                        accountId=response['data']['createAccount']['id']
                        messages.success(request,"Successfuly registerd")
                        return redirect('complete-profile',account_id=accountId)
                    else:
                        print("Unexpected erros occurred")
                        messages.error(request,"Unexpected erros occurred")   
                        return JsonResponse(response)
                else:
                    print("Password musb be atleast 5")   
                    messages.error(request,"Password musb be atleast 5") 
            else:
                print("Password dont match ")
                messages.error(request,"Password dont match ") 
        else:
            print("Email is invalid check again") 
            messages.error(request,"Email is invalid check again")    
    return render(request,'signup.html')

#complete profile function
def completeProfile(request,account_id):
    if request.method == "POST":
        name = request.POST.get("name")
        region = request.POST.get("region")
        ward = request.POST.get("ward")
        phone = request.POST.get("phone")
        profession = request.POST.get("profession")
        

        mutation = """
            mutation CreateUser($input: CreateUserInput!) {
                createUser(createUserInput: $input) {
                    id
                    email
                    profession
                    phone
                }
            }
        """

        variables = {
            "input": {
                "name": name,
                "region": region,
                "ward": ward,
                "phone": phone,
                "profession": profession,
                "accountId": account_id
            }
        }

        response = api.performMuttion(mutation,variables)
        if 'errors' in response:
            print("Errors encounterd")
            messages.error(request,response['errors'][0]['message'])
        
        elif 'data' in response:
            print(response,'successfully')
            messages.success(request,"Successfuly updated")

            #redirect the user to the login page 
            return redirect('login')
        else:
            print("Netwwork issues")
            messages.error(request,"Netwwork issues")

    return render(request,'complete-profile.html')

#email validator function
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)