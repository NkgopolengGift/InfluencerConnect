from . import views
from django.urls import path

urlpatterns = [

    path('', views.index, name='index'),

    path('signup/', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('signout/', views.signOut, name='signout'),
    path('admin_profile/',views.adminProfile, name='admin_profile'),

    path('sponser/', views.sponsorPlatform, name='sponser'),
    path('influencer/', views.influencerPlatform, name='influencer'),

    path('home/', views.home, name='home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    #path('summary/', views.summary_report, name='summary'),
    #path('csv_report', views.export_csv, name='csv_report'),

    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name="delete_account"),
    
]