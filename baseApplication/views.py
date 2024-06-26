import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import instaloader
from django.core.mail import send_mail, BadHeaderError
from .utils import fetch_youtube_channel_data, fetch_instagram_profile
from .models import *
from .forms import ChatMessagesCreateform
from django.http import JsonResponse
from django.urls import reverse
import json

from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse

import string
import random
from datetime import datetime

###########For Reports#######
import io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from docx import Document

#############-For YouTube API-##################
from decouple import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#############-For YouTube API-##################
from django.views.decorators.http import require_POST


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

        if User.objects.filter(username=username).exists():
            messages.error(request, "User exists. Login")
            return render(request, '404.html')
        elif  User.objects.filter(email=email).exists():
            messages.error(request, "Email exists.")
            return render(request, '404.html')
        new_user = User(
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
####################################################
def resertPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
                token = 'generate_your_token_here'
                user.password_reset_token = token
                user.save()
                return render(request, 'email_error_page.html')
        else:
            return render(request, 'email_error_page.html')
    return render(request,'resert_password.html')
####################################################
def newPassword(request):
    return render(request,'new_password.html')
####################################################
def resertDone(request):
    return render(request,'resert_done.html')
#############-Create Admin Profile-##################
def adminProfile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phoneNumber')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User exists. Login")
            return render(request, 'signin.html')

        new_user = User(
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
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signup')

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

#############-Influecer-##################
def influencerPlatform(request):
    if request.method == 'POST':
        youtube_url = request.POST.get('youtube_url')
        instagram_url = request.POST.get('instagram_url')
        content_category = request.POST.get('content_category')
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('signup')
          
        new_influencer = Influencer(
            user=user,
            content_category=content_category,
        )
        new_influencer.save()

        if youtube_url and youtube_url.strip():
            try:
                Platform.objects.create(influencer=new_influencer, platform_name="YouTube", platform_url=youtube_url.strip())
            except IntegrityError:
                return render(request, 'platform_error.html')
        
        if instagram_url and instagram_url.strip():
            try:
                Platform.objects.create(influencer=new_influencer, platform_name="Instagram", platform_url=instagram_url.strip())
            except IntegrityError:
                return render(request, 'platform_error.html')
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

                if user.is_admin:
                    return redirect('admin_home')
                else:
                    if not check_payment_status(user):
                        return redirect('initiate_payment')
                    #messages.success(request, 'You have logged in successfully.')
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
  
    platforms = Platform.objects.select_related('influencer__user').all()
    data = {}

    for platform in platforms:
        
        influencer_id = platform.influencer.user.user_id
        logged_in_user_id = request.user.user_id 

        if influencer_id not in data:
            data[influencer_id] = {
                'influencer_username': platform.influencer.user.username,
                'youtube_data': {},
                'instagram_data': {},
                'influencer_id': influencer_id,
                'logged_in_user_id': logged_in_user_id,
            }

        if platform.platform_name == 'YouTube':
            channel_url = platform.platform_url
            youtube_data = fetch_youtube_channel_data(channel_url)
            data[influencer_id]['youtube_data'] = youtube_data
        elif platform.platform_name == 'Instagram':
            username = platform.platform_url.split('/')[-1]
            instagram_data = fetch_instagram_profile(username)
            data[influencer_id]['instagram_data'] = instagram_data

    context = {
        
        'username': request.user.username,
        'platform_data': data.values(),
        
    }
    return render(request, 'home.html', context)
#############-Generate payment report-##################

def process_payments():
    paid_users = Payment.objects.filter(verified=True).values_list('user__username', flat=True)
    all_users = User.objects.all().values_list('username', flat=True)
    
    paid_usernames = set(paid_users)
    unpaid_usernames = set(all_users) - paid_usernames
    
    return list(paid_usernames), list(unpaid_usernames)


def generate_pdf_report(request):
    paid_usernames, unpaid_usernames = process_payments()
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "User Payment Report")
    p.drawString(100, 730, "Paid Users:")
    
    y = 710
    for username in paid_usernames:
        p.drawString(100, y, username)
        y -= 20
    
    p.drawString(100, y - 20, "Unpaid Users:")
    y -= 40
    for username in unpaid_usernames:
        p.drawString(100, y, username)
        y -= 20
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="user_payment_report.pdf"'
    return response

def generate_word_report(request):
    paid_usernames, unpaid_usernames = process_payments()
    
    doc = Document()
    doc.add_heading('User Payment Report', 0)

    doc.add_heading('Paid Users:', level=1)
    for username in paid_usernames:
        doc.add_paragraph(username)

    doc.add_heading('Unpaid Users:', level=1)
    for username in unpaid_usernames:
        doc.add_paragraph(username)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=user_payment_report.docx'
    return response

def generate_excel_report(request):
    paid_usernames, unpaid_usernames = process_payments()
    
    df_paid = pd.DataFrame(paid_usernames, columns=['Paid Users'])
    df_unpaid = pd.DataFrame(unpaid_usernames, columns=['Unpaid Users'])
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_paid.to_excel(writer, sheet_name='Paid Users', index=False)
        df_unpaid.to_excel(writer, sheet_name='Unpaid Users', index=False)

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=user_payment_report.xlsx'
    return response

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
            sponsor = Sponsor.objects.get(user=user)
        except Sponsor.DoesNotExist:
            sponsor = None
    elif user.account_type == 'INFLUENCER':
        try:
            influencer = Influencer.objects.get(user=user)
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
        if User.objects.exclude(pk=user.pk).filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('update_profile')
        if User.objects.exclude(pk=user.pk).filter(email=email).exists():
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
            if Sponsor.objects.exclude(user=user).filter(website=website_url).exists():
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

#############-Delete account-##################
def delete_account(request):
    if request.method == 'GET':
        user = request.user
        
        if user.account_type == 'SPONSOR':
           try:
                sponsor_data = Sponsor.objects.filter(user=user)
                sponsor_data.delete()
           except Sponsor.DoesNotExist:
                pass 
           
        elif user.account_type == 'INFLUENCER':
            try:
                platforms = Platform.objects.filter(influencer_id__user=user)
                platforms.delete()
                
                influencer = Influencer.objects.get(user=user)
                influencer.delete()
            except Sponsor.DoesNotExist:
                pass 

        user.delete()

        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home')
    else:
        return render(request, 'delete_account.html')

#############-Initializing payment-##################
def initiate_payment(request):
    context = {
        'PAYSTACK_PUBLIC_KEY': settings.PAYSTACK_PUBLIC_KEY,
        'email': request.user.email  # Assuming user is authenticated and has an email
    }
    return render(request, 'payment_form.html',context)

#############-Verify payment-##################
#@login_required(login_url='signin')
def verify_payment(request):
     
    reference = request.GET.get('reference')
    print(reference)
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
    
#############-Generate payment report-##################
def payment_report(request):
    payments = Payment.objects.all()
    context = {
        'payments': payments
    }
    return render(request, 'admin_home.html', context)




def chat_room(request, room_name):
    return render(request, 'chat.html', {
        'room_name': room_name
    })

#############-messaging view-##################
@login_required
def create_room(request):
    if request.method == 'POST':
        influencer_id = request.POST.get('influencer_id')
        sponsor_id = request.POST.get('sponsor_id')

        influencer = Influencer.objects.get(user=influencer_id)
        influencer_pk = influencer.pk
    
        sponsor = Sponsor.objects.get(user=sponsor_id)
        sponsor_pk = sponsor.pk
        
        room = Room.objects.filter(influencer=influencer_pk, sponsor=sponsor_pk).first()
        if room:
           
            return redirect('chat')
        else:
            room = Room.objects.create(influencer=influencer, sponsor=sponsor)
            return redirect('chat')
        

    else:
        return render(request, 'messages.html')

    
####################################################
@login_required
@require_POST
def accept_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user != room.influencer.user_id:
        return JsonResponse({'error': 'You are not authorized to accept this room.'}, status=403)
    room.accepted = True
    room.save()
    return JsonResponse({'success': True})

@login_required
@require_POST
def send_message(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        content = request.POST.get('content')
        room = Room.objects.get(room_id=room_id)
        message = Message.objects.create(
            room=room,
            user=request.user,
            content=content
        )
        return JsonResponse({'status': 'success', 'message': 'Message sent successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def get_messages(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user != room.influencer.user_id and request.user != room.sponsor.user_id:
        return JsonResponse({'error': 'You are not authorized to view messages in this room.'}, status=403)
    messages = room.messages.order_by('timestamp').values('sender__username', 'content', 'timestamp')
    return JsonResponse(list(messages), safe=False)

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.user != room.influencer.user_id and request.user != room.sponsor.user_id:
        return redirect('home')

    if request.method == 'POST' and 'accept' in request.POST:
        if request.user == room.influencer.user_id:
            room.accepted = True
            room.save()
            messages.success(request, 'Room accepted. You can now start chatting.')
        else:
            messages.error(request, 'You are not authorized to accept this room.')

    return render(request, 'chat_room.html', {'room': room})

@login_required
def chat_rooms(request):
    user = request.user

    # Fetch rooms where the user is either a sponsor or an influencer
    influencer_rooms = Room.objects.filter(influencer__user_id=user)
    sponsor_rooms = Room.objects.filter(sponsor__user_id=user)
    
    context = {
        'influencer_rooms': influencer_rooms,
        'sponsor_rooms': sponsor_rooms,
    }
    return render(request, 'chat_rooms.html', context)
##############################################################
def my_view(request):
    return render(request, '404.html')
###############################################################
def chat(request):
    user = request.user
    if user.account_type == "INFLUENCER":
        rooms = Room.objects.filter(influencer__user=user)
    else:
        rooms = Room.objects.filter(sponsor__user=user)
    
    room_messages = {}
    for room in rooms:
        messages = Message.objects.filter(room=room).order_by('timestamp')
        room_messages[room] = messages
    
    context = {
        'rooms': rooms,
        'room_messages': room_messages,
    }
    return render(request, 'messages.html', context)
#####################################################
def fetch_messages(request):
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Room, pk=room_id)
    messages = Message.objects.filter(room=room).order_by('timestamp')

    message_data = []
    for message in messages:
        message_data.append({
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'user': message.user.username 
        })

    return JsonResponse(message_data, safe=False)