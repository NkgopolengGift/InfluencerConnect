from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),

    path('signup/', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('signout/', views.signOut, name='signout'),

    path('sponser/', views.sponsorPlatform, name='sponser'),
    path('influencer/', views.influencerPlatform, name='influencer'),

    path('home/', views.home, name='home'),
    #path('summary/', views.summary_report, name='summary'),
    #path('csv_report', views.export_csv, name='csv_report'),

    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name="delete_account"),
    
]