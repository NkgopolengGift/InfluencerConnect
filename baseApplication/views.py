import requests
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from .models import UserTBL, Sponsor, Influencer, Platform, Payment, Chat
from django.http import JsonResponse
from django.urls import reverse

from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse

import string
import random
from datetime import datetime

#############-For YouTube API-##################
from decouple import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#############-For YouTube API-##################


import random
from datetime import datetime, timedelta

def index(request):
    return render(request, 'index.html')

#############-sign up-##################
def signUp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        account_type = request.POST.get('type')

        if UserTBL.objects.filter(username=username).exists():
            messages.error(request, "User exists. Login")
            return render(request, 'signin.html')

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

#############-Create Admin Profile-##################
def adminProfile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')

        if UserTBL.objects.filter(username=username).exists():
            messages.error(request, "User exists. Login")
            return render(request, 'signin.html')

        new_user = UserTBL(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=make_password(password), 
            is_admin=True
        )
        
        new_user.save()
        messages.success(request,'You have successfully created an account. Login')
        return render(request, 'signin.html')
    return render(request, 'admin_profile.html')

#############-Sponser##################
def sponsorPlatform(request):
    if request.method == 'POST':
        content_category = request.POST.get('content_category')
        website = request.POST.get('website')
        username = request.POST.get('username')

        try:
            user = UserTBL.objects.get(username=username)
        except UserTBL.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signup')

        new_sponsor = Sponsor(
            user_id=user,
            content_category=content_category,
            website=website,
        )
        new_sponsor.save()

        messages.success(request, "Your account is set up successfully. Login")
        return redirect('signin')
    else:
        return render(request, 'signin.html')

#############-Influecer-##################
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

        new_influencer = Influencer(
            user_id=user,
            content_category=content_category,
        )
        new_influencer.save()
   
        new_platform = Platform(
            influencer_id=new_influencer,
            platform_name=platform_name,
            platform_url=platform_url,
        )
        new_platform.save()

        messages.success(request, "Your account is active. Login")
        return redirect('signin')
    else:
        return render(request, 'signin.html')

#############-log in-##################
def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged in successfully.')

                if user.is_admin:
                    return redirect('admin_home')
                else:
                    if not check_payment_status(user):
                        return redirect('initiate_payment')
                    return redirect('home')
            else:
                messages.error(request, 'Invalid credentials, try again.')
                return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

#############-log out-##################
def signOut(request):
    logout(request)
    messages.success(request,'You have logged out')
    return redirect('index')

def sponser(request):
    return render(request, 'sponser.html')
    
#############-home-##################
@login_required(login_url='index')
def home(request):
  
    platforms = Platform.objects.select_related('influencer_id__user_id').all()
    youtube_data = []

    for platform in platforms:
        if platform.platform_name == 'YouTube':
            channel_url = platform.platform_url
            # Get YouTube channel data
            channel_data = get_youtube_channel_data(channel_url)

            if channel_data:
                # Store channel data along with influencer username
                youtube_data.append({
                    'influencer_username': platform.influencer_id.user_id.username,
                    'channel_data': channel_data
                })
              
    context = {
        'username': request.user.username,
        'youtube_data': youtube_data
    }
    return render(request, 'home.html', context)

#############-Admin home-##################
@login_required(login_url='index')
def admin_home(request):

    return render(request, 'admin_home.html')


#############-Profile-##################
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

#############-Profile-##################
@login_required(login_url='index')
def update_profile(request):
    user = request.user

    # Fetch user's related data based on account_type
    if user.account_type == 'SPONSOR':
        try:
            sponsor = Sponsor.objects.get(user_id=user)
        except Sponsor.DoesNotExist:
            sponsor = None
    elif user.account_type == 'INFLUENCER':
        try:
            influencer = Influencer.objects.get(user_id=user)
            platforms = Platform.objects.filter(influencer_id=influencer)
        except Influencer.DoesNotExist:
            influencer = None
            platforms = None

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')

        # Check if username or email already exist for other users
        if UserTBL.objects.exclude(pk=user.pk).filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('update_profile')
        if UserTBL.objects.exclude(pk=user.pk).filter(email=email).exists():
            messages.error(request, 'Email is already taken. Please choose a different one.')
            return redirect('update_profile')

        # Update user data
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.save()

        if user.account_type == 'SPONSOR':
            website_url = request.POST.get('website_url')

            # Check if the new website URL already exists for other sponsors
            if Sponsor.objects.exclude(user_id=user).filter(website=website_url).exists():
                messages.error(request, 'Website URL is already used by another sponsor.')
                return redirect('update_profile')

            sponsor.website = website_url
            sponsor.save()

            if user.account_type == 'INFLUENCER':
                influencer = user.influencer
                # Handle existing platforms
                for platform in influencer.platforms.all():
                    platform_url = request.POST.get(f'platform_{platform.pk}')
                    if platform_url:
                        platform.platform_url = platform_url
                        platform.save()

                # Handle new platforms
                new_platform_count = 0
                while True:
                    platform_name = request.POST.get(f'new_platform_name_{new_platform_count}')
                    platform_url = request.POST.get(f'new_platform_url_{new_platform_count}')
                    if platform_name and platform_url:
                        Platform.objects.create(influencer=influencer, platform_name=platform_name, platform_url=platform_url)
                        new_platform_count += 1
                    else:
                        break

        messages.success(request, 'Profile updated successfully.')
        return redirect('update_profile')

    else:
        # Prepopulate form with existing data
        context = {
            'user': user,
            'sponsor': sponsor if user.account_type == 'SPONSOR' else None,
            'influencer': influencer if user.account_type == 'INFLUENCER' else None,
            'platforms': platforms if user.account_type == 'INFLUENCER' else None,
        }
        return render(request, 'update_profile.html', context)

#############-Charting-##################
@login_required(login_url='index')
def chat(request):
    return  render(request, 'chat.html')
#############-Delete account-##################
def delete_account(request):
    if request.method == 'GET':
        user = request.user
        
        if user.account_type == 'SPONSOR':
           try:
                sponsor_data = Sponsor.objects.filter(user_id=user)
                sponsor_data.delete()
           except Sponsor.DoesNotExist:
                pass 
           
        elif user.account_type == 'INFLUENCER':
            try:
                platforms = Platform.objects.filter(influencer_id__user_id=user)
                platforms.delete()
                
                influencer = Influencer.objects.get(user_id=user)
                influencer.delete()
            except Sponsor.DoesNotExist:
                pass 

        user.delete()

        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    else:
        return render(request, 'delete_account.html')

#############-Feaching YouTube data-##################
def get_youtube_channel_data(channel_url):

    # Initialize the YouTube Data API client
    api_key = settings.YOUTUBE_API_KEY
    youtube = build('youtube', 'v3', developerKey=api_key)

    channel_id = channel_url.split('/')[-1]
    try:
        # Call the channels.list method to retrieve channel statistics
        details_response = youtube.channels().list(
            part='statistics,snippet,contentDetails',
            id=channel_id
        ).execute()
        
        if 'items' in details_response:

            channel = details_response['items'][0]
            snippet = channel['snippet']
            statistics = channel['statistics']
            uploads_playlist_id = channel['contentDetails']['relatedPlaylists']['uploads']

            channel_title = snippet.get('title', '')
            creation_date = snippet.get('publishedAt', '')
            views = statistics.get('viewCount', 0)
            subscribers = statistics.get('subscriberCount', 0)
            videos = statistics.get('videoCount', 0)

            # Initialize totals
            total_likes = 0
            total_comments = 0

            # Retrieve all videos in the uploads playlist
            next_page_token = None
            while True:
                playlist_response = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=uploads_playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()
                
                video_ids = [item['contentDetails']['videoId'] for item in playlist_response['items']]

                # Get statistics for each video
                video_response = youtube.videos().list(
                    part='statistics',
                    id=','.join(video_ids)
                ).execute()

                for video in video_response['items']:
                    video_stats = video['statistics']
                    total_likes += int(video_stats.get('likeCount', 0))
                    total_comments += int(video_stats.get('commentCount', 0))

                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break

            channel_data = {
                'likes': total_likes,
                'views': views,
                'subscribers': subscribers,
                'comments': total_comments,
                'videos': videos,
                'channel_title': channel_title,
                'creation_date': creation_date
            }

            # Update Platform model with fetched data
            platform = Platform.objects.get(platform_url=channel_url)
            platform.likes = total_likes
            platform.views = views
            platform.subscribers = subscribers
            platform.comments = total_comments
            platform.videos = videos
            platform.save()
            return channel_data
       
        else:
            print('No items found in YouTube API response:', details_response)
            return None
    except HttpError as e:
        print('An HTTP error occurred:', e)
        return None
    except HttpError as e:
        print('An error occurred:', e)
        return None
    

#############-Initializing payment-##################
def initiate_payment(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        amount = request.POST.get('amount')
        
        reference = generate_reference() 
        print(reference)
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            "email": email,
            "amount": int(amount) * 100,
            "reference": reference,
            "callback_url": request.build_absolute_uri(reverse('verify_payment')),
        }
        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
        response_data = response.json()

        if response_data.get('status') == True:
            auth_url = response_data['data']['authorization_url']
            return JsonResponse({'auth_url': auth_url})
        else:
            messages.error(request, 'Payment initialization failed')
            return JsonResponse({'error': 'Payment initialization failed'})
    else:
        email = request.user.email  
        return render(request, 'payment_form.html', {'email': email})

#############-Verify payment-##################
#@login_required(login_url='signin')
def verify_payment(request):
     
    reference = request.GET.get('reference')
    
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
    response_data = response.json()

    if response_data['status'] == True and response_data['data']['status'] == 'success':
        amount = response_data['data']['amount'] / 100
        Payment.objects.create(
            user=request.user,
            reference=reference,
            amount=amount,
            verified=True,
        )
        #Payment.save()
        messages.success(request, 'Payment successful')
        return redirect('home')
    else:
        messages.error(request, 'Payment verification failed')
        return redirect('initiate_payment')
#############-Gererate Reference-##################
def generate_reference():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{timestamp}{random_chars}"

#############-Check payment status-##################
def check_payment_status(user):
    try:      
        last_payment = Payment.objects.filter(user=user).latest('transaction_date')
        if last_payment.transaction_date >= timezone.now() - timedelta(days=30):
            return True
        else:
            return False
    except Payment.DoesNotExist:
        return False