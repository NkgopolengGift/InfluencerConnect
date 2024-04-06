from django.forms import ModelForm
from .models import UsersTBL

class UsersTblForm(ModelForm):
    class Meta:
        model = UsersTBL  
        fields = ['username', 'email', 'phone_number','account_type']