from . import views
from django.urls import path

urlpatterns = [

    path('', views.index, name='index'),

    path('signup/', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('signout/', views.signOut, name='signout'),
    path('admin_profile/',views.adminProfile, name='admin_profile'),
    path('resert_password/',views.resertPassword, name='resert_password'),
    
    path('new_password/',views.newPassword, name='new_password'),
    path('resert_done/',views.resertDone, name='resert_done'),

    path('sponser/', views.sponsorPlatform, name='sponser'),
    path('influencer/', views.influencerPlatform, name='influencer'),

    path('home/', views.home, name='home'),
    path('admin_home/', views.admin_home, name='admin_home'),

    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_account/', views.delete_account, name="delete_account"),

    path('initiate_payment/', views.initiate_payment, name="initiate_payment"),
    path('verify_payment/', views.verify_payment, name='verify_payment'),

    path('payment_report/', views.payment_report, name='payment_report'),

    path('chat/', views.chat, name='chat'),
    path('create_room/', views.create_room, name='create_room'),
    path('send_message/', views.send_message, name='send_message'),
    path('fetch-messages/', views.fetch_messages, name='fetch_messages'),
    path('my-view/', views.my_view, name='my_view'),

]