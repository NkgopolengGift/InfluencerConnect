from django.urls import path
from . import views

urlpatterns = [

    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),

    path('', views.start, name='start'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('adminpage/', views.adminpage, name='adminpage'),
    
    
]