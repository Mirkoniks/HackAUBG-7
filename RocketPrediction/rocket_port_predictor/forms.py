from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage, MissionInput

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default help text
        for field in self.fields:
            self.fields[field].help_text = None

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class MissionForm(forms.ModelForm):
    # Define choices for destinations
    DESTINATION_CHOICES = [
        ('LEO', 'Low Earth Orbit'),
        ('MEO', 'Medium Earth Orbit'),
        ('GEO', 'Geosynchronous Orbit'),
        ('Moon', 'Moon'),
        ('Mars', 'Mars'),
        ('Unknown', 'Unknown'),
    ]

    destination = forms.ChoiceField(choices=DESTINATION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = MissionInput
        fields = ['rocket_name', 'launch_date', 'cost_million', 'destination']
        widgets = {
            'rocket_name': forms.TextInput(attrs={'class': 'form-control'}),
            'launch_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cost_million': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.1}),
        } 