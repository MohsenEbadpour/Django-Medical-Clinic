from django import forms
from .models import User,Sick,Doctor
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput,label="Email")
    password = forms.CharField(widget=forms.PasswordInput,label="Password")

    def clean_password(self):
        password = self.cleaned_data['password']
        email = self.cleaned_data['email'].lower()
        users = User.objects.filter(email=email)
        if users.count() :
            user = User.objects.get(email=email)
            if user.check_password(password):
                return password
            else :
                raise ValidationError("گذرواژه شما صحیح نمی باشد")
        else : 
            raise ValidationError("کاربری با این اطلاعات یافت نشد")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        return email


class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput,label="Email")
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    name = forms.CharField()
    id_number = forms.IntegerField()
    phone = forms.IntegerField()

    def clean_email(self): 
        email = self.cleaned_data['email'].lower()
        exists = User.objects.filter(email=email)
        if exists.count():
            raise ValidationError("این ایمیل از قبل ثبت نام شده است")
        return email
 
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password)<4:
                raise ValidationError("گذرواژه حداقل باید شامل 4 کاراکتر باشد")
        return password



class EditForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput,label="Email")
    password = forms.CharField(widget=forms.PasswordInput,label="Password")
    name = forms.CharField()
    id_number = forms.IntegerField()
    phone = forms.IntegerField()
 
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password)<4:
                raise ValidationError("گذرواژه حداقل باید شامل 4 کاراکتر باشد")
        return password
    
    
        