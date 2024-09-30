from django import forms
from .models import FacultyInfo
from django.contrib.auth.models import User

class FacultyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'id': 'passwordfield', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'id': 'emailfield', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'id': 'usernamefield', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Enter your username.'
        self.fields['email'].help_text = 'Enter your email address.'
        self.fields['password'].help_text = 'Enter a strong password.'

class FacultyInfoForm(forms.ModelForm):
    class Meta:
        model = FacultyInfo
        fields = ['address', 'subject', 'picture']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(FacultyInfoForm, self).__init__(*args, **kwargs)
        self.fields['address'].help_text = 'Enter your address.'
        self.fields['subject'].help_text = 'Enter the subject you teach.'
        self.fields['picture'].help_text = 'Upload a profile picture (optional).'
