from django.forms import ModelForm
from django import forms 
from .models import *

class ChatMessagesCreateform(ModelForm):
    class Meta:
        model  = Message
        fields = ['content']
        widgets= {
            'content': forms.TextInput(attrs={'placeholder':'send a message','class':'','maxlength':'300','autofocus':True}),
        }