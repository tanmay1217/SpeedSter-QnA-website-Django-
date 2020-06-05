from django import forms
from django.core import validators
from django.contrib.auth.models import User
class user_create(forms.Form):
    user_name = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label ='E-mail(optional)', widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}),required=False)
    password = forms.CharField(label = 'Password' ,min_length=8,max_length=32,widget =forms.TextInput(attrs={'type': 'password','placeholder':'Password'}))
    c_password = forms.CharField(label = 'Password',widget = forms.TextInput(attrs={'type': 'password','placeholder':'Password(again)'}))

    def clean(self):
        all_clean=super().clean()
        if all_clean['password'] != all_clean['c_password']:
            raise forms.ValidationError("password didn't match")
        #print(all_clean['email'])
        email_check = all_clean['email']
        if User.objects.filter(email =email_check).exists():
            raise forms.ValidationError("The email you entered has already been taken. Please try another email id")
        user_name_check =all_clean['user_name']
        if User.objects.filter(username =user_name_check).exists():
            raise forms.ValidationError("The username you entered has already been taken. Please try another username")


    '''
    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
       return self.cleaned_data'''

    '''def clean_username(self):
        user_name = self.cleaned_data.get('user_name')
        if User.objects.filter(username__iexact=user_name).exists():
            raise forms.ValidationError('Username already exists')
        return user_name
        '''
