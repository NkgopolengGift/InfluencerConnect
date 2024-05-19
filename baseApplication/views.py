from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserTBL
from .models import Sponsor
from .models import Influencer
from .models import Platform

#####################-START PAGE-####################### 
def index(request):
    return render(request, 'index.html')

#####################-Sign Up-####################### 
def signUp(request):
    if request.method == 'POST':
       
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        account_type = request.POST.get('type')

        # Check if the username
        if UserTBL.objects.filter(username=username).exists():
            messages.error(request, "User exists. Login")
            return render(request, 'signin.html')

        # Create new user object
        new_user = UserTBL(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=make_password(password), 
            account_type=account_type,
        )
        
        new_user.save()
        context = {'username': username, 'account_type': account_type}
        return render(request, 'platform.html', context)
    return render(request, 'signup.html')

#####################-Enter Sponor Details-####################### 
def sponsorPlatform(request):
    if request.method == 'POST':
       
        content_category = request.POST.get('content_category')
        website = request.POST.get('website')
        username = request.POST.get('username')

        # Check if the user exists in UserTBL
        try:
            user = UserTBL.objects.get(username=username)
        except UserTBL.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signup')

        # Create new Sponsor record
        new_sponsor = Sponsor(
            user=user,
            content_category=content_category,
            website=website,
        )
        new_sponsor.save()

        messages.success(request, "Your account is set up successfully. Login")
        return redirect('signin')
    else:
        return render(request, 'signin.html')
    
#####################-Enter Influencer Details-####################### 
def influencerPlatform(request):
    if request.method == 'POST':
       
        platform_name = request.POST.get('platform_name')
        platform_url = request.POST.get('platform_url')

        content_category = request.POST.get('content_category')
        username = request.POST.get('username')

        try:
            user = UserTBL.objects.get(username=username)
        except UserTBL.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signup')

        # Create new Influencer record
        new_influencer = Influencer(
            user=user,
            username=username,
            content_category=content_category,
        )
        new_influencer.save()

        # Create new Platform record
        new_platform = Platform(
            user_id=new_influencer,
            platform_name=platform_name,
            platform_url=platform_url,
        )
        new_platform.save()

        messages.success(request, "Your account is active. Login")
        return redirect('signin')
    else:
        return render(request, 'signin.html')

#####################-Sign In-####################### 
def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials, try again.')
                return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

#####################-Sign out-#######################
def signOut(request):
    logout(request)
    messages.success(request,'You have logged out')
    return redirect('index')


#####################-SPONSER-####################### 
def sponser(request):
    return render(request, 'sponser.html')
    
#####################-HOME PAGE-#######################
@login_required(login_url='index')
def home(request):
    context = {'username': request.user.username}
    return render(request, 'home.html', context)

#####################-ADMIN PAGE-#######################
@login_required(login_url='index')
def adminpage(request):
    context = {'username': request.user.username}
    return render(request, 'adminpage.html', context)

#####################-UPDATE PROFILE-#######################
@login_required(login_url='index')
def profile(request):
    if request.method == 'POST':
    
        user = request.user
       
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        
        user.username = username
        user.email = email
        user.phone_number = phone_number
        
        user.save()

        messages.success(request, 'Your profile has been updated!')
        return redirect('home')
    else:
        return render(request, 'profile.html')
#####################-DELETE PROFILE-#######################
def delete_account(request):
    if request.method == 'POST':
        # Retrieve the current user based on the session
        user = request.user
        # Perform the deletion of the user and any related data
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        # Redirect to the home page or login page after deletion
        return redirect('home')
    else:
        # If not a POST request, render the delete confirmation page
        return render(request, 'delete_account.html')


