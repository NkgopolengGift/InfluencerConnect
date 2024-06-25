from django.contrib import admin
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from .models import UserProfile

# Register your models here.
from .models import *   

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Room)


##########Admin block Function ##############################

# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'Profile'

# class CustomUserAdmin(UserAdmin):
#     inlines = (UserProfileInline, )
#     list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_blocked')

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)