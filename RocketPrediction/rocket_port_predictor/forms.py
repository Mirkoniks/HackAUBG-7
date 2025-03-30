from django import forms
from .models import ContactMessage, MissionInput

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