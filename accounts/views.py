from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feedback
import re
from django.http import HttpResponseRedirect, HttpResponse
import africastalking
from django.conf import settings
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt  

africastalking.api_key= settings.AFRICASTALKING_API_KEY

# Create your views here.


def account(request):
    return render(request, 'accounts/loginform.html')  # render login form


def login(request):
    user_name = request.POST['loginemail']
    password = request.POST['loginPassword']
    # ------------------------------
    values = {
        'user_name': user_name,
    }
    # ------------------------------
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  # mail format
    if re.search(regex, user_name):  # imported re | checking the mail format
        user = auth.authenticate(email=user_name, password=password)  # taking mail as user_name
    else:
        user = auth.authenticate(username=user_name, password=password)
    if user is not None:  # user created
        auth.login(request, user)  # loged in
        return redirect('/')  # to home
    else:
        message = {
            'from': 'login',
            'error': 'Invalid Credentials',
            'value': values
        }
        return render(request, 'accounts/loginform.html', message)
    # return render(request, './accounts/login.html', {'data': 'login is successful'})


def register(request):  # getting new user info
    user_name = request.POST['userid']
    full_name = request.POST['name']
    email = request.POST['emailAdress']
    phone = request.POST['phone']
    password = request.POST['password']
    # -----------------------------------
    values = {
        'user_name': user_name,
        'full_name': full_name,
        'email': email,
        'phone':phone,
    }
    # -----------------------------------
    # detect the number of words in fullname
    
    length_of_fullname = len(full_name.split())
    if length_of_fullname == 1:
        first_name = full_name
        last_name = ''
    else:
        first_name, last_name = full_name.rsplit(maxsplit=1)  # splitting name as reverse order

    if User.objects.filter(username=user_name).exists():  # checking user name from database
        message = {
            'from': 'signup',
            'error': 'User name is already taken',
            'values': values  # to stay in form
        }
        return render(request, 'accounts/loginform.html', message)  # return with message

    elif User.objects.filter(email=email).exists():  # checking email from database
        message = {
            'from': 'signup',
            'error': 'Email is already taken',
            'values': values  # to stay in form
        }
        return render(request, 'accounts/loginform.html', message)  # return with message

    else:
        user = User.objects.create_user(username=user_name, password=password, email=email, first_name=first_name,
                                        last_name=last_name)
        user.save()
        # After registration auto login the user and redirect to home page
        user = auth.authenticate(username=user_name, password=password)
        auth.login(request, user)
        africastalking_username = 'lyzy'
        africastalking_api_key = africastalking.api_key
            
        africastalking.initialize(africastalking_username, africastalking_api_key)
        sms = africastalking.SMS
        message = "Welcome to NiLocate Transport Services."
        response = sms.send(message, [phone])
        #print(profile.contact_number)
        print("SMS response:", response)
        return redirect('/')  # to home
    # return render(request, 'accounts/login.html', {'data': 'registration is successful'})


def logout(request):
    auth.logout(request)
    return redirect('/')  # to home


def feedback(request):
    forms = request.POST
    name = request.POST['name']
    email = request.POST['email']
    subject = request.POST['subject']
    message = request.POST['message']
    msg = Feedback(name=name, email=email, subject=subject, message=message)
    msg.save()
    print(forms)
    return HttpResponse("Message sent successfully!!")


@csrf_exempt
def send_whatsapp_message(request):
    #account_sid = 'AC8d51a8e966e5a7d3a23f71dc88ea1efa'
    account_sid = ''
   # auth_token = '83e2ed006bb6754285cf84fe10c4c97c'
    auth_token = ''
    client = Client(account_sid, auth_token)

    message = request.POST['Body']
    print(message)
    sender_name = request.POST['ProfileName']
    sender_number = request.POST['From']

    if message == "hi":
        client.messages.create(
            from_='whatsapp:+14155238886',
            body='Welcome to our services.\nMy name is Aloo, your assistant today.\n1.Do you want to know more about traffic rules..\n 2. Do you want to know more about traffic violations ',
            to=sender_number
    
        )
       

    if message == "1":
        client.messages.create(
            from_='whatsapp:+14155238886',
            body='Are you a driver or a pedestrian?',
            to=sender_number
    
        )

    if message == "driver":
        client.messages.create(
            from_='whatsapp:+14155238886',
            body='Certainly:\n 1. Obey signals and signs (traffic lights, stop signs).\n2. Yield to pedestrians (especially at crosswalks).\n3. Adhere to speed limits (posted for safety).\n4. Signal when turning (to alert other drivers).\n5. Maintain a safe distance (from vehicles ahead).\n6. Stop for school buses (when lights are flashing).\n7. Yield when needed (at intersections or merges).\n8. Stay focused, avoid distractions (to prevent accidents).\n9. Drive sober (alcohol and drugs impair driving).\n10. Buckle up (seatbelts save lives).',
            to=sender_number
    
        )

    if message == "pedestrian":
        client.messages.create(
            from_='whatsapp:+14155238886',
            body='Certainly:\n1. Use crosswalks when available.\n2. Obey pedestrian signals.\n3. Look both ways before crossing.\n4. Walk facing traffic when no sidewalk.\n5. Avoid distractions like phones.\n6. Yield to vehicles when necessary.\n7. Use designated paths where possible.\n8. Cross promptly, but safely.\n9. Be visible, especially at night.\n10. Stay aware of surroundings.',
            to=sender_number
    
        )
    

    if message == "2":
        client.messages.create(
            from_='whatsapp:+14155238886',
            body='In Kenya, some common traffic violations and their associated penalties include:\n1. **Speeding**: Fines ranging from Ksh 500 to Ksh 10,000 depending on the speed exceeded, and potential license suspension or imprisonment for extreme cases.\n2. **Running red lights or stop signs**: Fines ranging from Ksh 3,000 to Ksh 10,000, potential license suspension, and points on the drivers record.\n3. **Driving under the influence (DUI)**: Fines starting from Ksh 100,000, license suspension, and potential imprisonment.\n4. **Failure to yield**: Fines ranging from Ksh 2,000 to Ksh 10,000, and potential points on the drivers record.\n5. **Illegal turns**: Fines ranging from Ksh 3,000 to Ksh 10,000, and potential license suspension.\n6. **Distracted driving**: Fines ranging from Ksh 10,000 to Ksh 30,000, and potential license suspension.\n7. **Driving without a license**: Fines starting from Ksh 7,000, vehicle impoundment, and potential imprisonment.\n8. **Driving with expired registration or without insurance**: Fines ranging from Ksh 3,000 to Ksh 10,000\n9. **Improper lane changes**: Fines ranging from Ksh 3,000 to Ksh 10,000, and potential license suspension.\n10. **Tailgating**: Fines ranging from Ksh 3,000 to Ksh 10,000, and potential license suspension.\n11. **Failure to use seat belts**: Fines ranging from Ksh 500 to Ksh 10,000 for both the driver and passengers.\n12. **Using a mobile phone while driving**: Fines ranging from Ksh 2,000 to Ksh 10,000, and potential license suspension.\n',
            to=sender_number
    
        )

    return HttpResponse( message)

def test(request):
    return render (request, 'accounts/base.html')
