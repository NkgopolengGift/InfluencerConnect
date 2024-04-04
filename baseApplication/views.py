from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import UsersTBL

##########################################################################################
#start page 
def start(request):
    return render(request, 'start.html')

##########################################################################################
#LogIn Page
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = UsersTBL.objects.get(username=username)
            if check_password(password, user.password):
                # Manually set the backend attribute
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                if user.account_type == 'admin':
                    return redirect('adminpage')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid  password.")
                return redirect('login_view')
        except UsersTBL.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('login_view')
    else:
        return render(request, 'login_view.html')
##########################################################################################
#LogOut
def logout_view(request):
    logout(request)
    return redirect('start')

##########################################################################################
#Create account page
def signup(request):
    if request.method == 'POST':
       
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        account_type = request.POST.get('type')

        # Check if the username
        if UsersTBL.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup_view.html')

        # Create new user object
        new_user = UsersTBL(
            username=username,
            email=email,
            phone_number=phone_number,
            password=make_password(password), 
            account_type=account_type,
        )
        
        new_user.save()
        messages.success(request, "Your account has been successfully created. LogIn")
        return redirect('login_view')

    else:
        return render(request, 'signup_view.html')
    
##########################################################################################
#Home Page
#@login_required(login_url ='login_view')
def home(request):
    return render(request, 'home.html')

##########################################################################################
#admin page
#@login_required(login_url ='login_view')
def adminpage(request):
    return render(request, 'adminpage.html')


