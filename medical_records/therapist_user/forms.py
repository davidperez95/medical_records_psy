from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Therapist
from django import forms

class RegisterUserForm(UserCreationForm):
    id = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=15)

    class Meta:
        model = Therapist
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            therapist = Therapist.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} is already in use')
    
    def clean_id(self):
        id = self.cleaned_data['id']
        try:
            therapist = Therapist.objects.get(id=id)
        except Exception as e:
            return id
        raise forms.ValidationError(f'Id {id} is already in use')
    
class LoginUserForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Therapist
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")

