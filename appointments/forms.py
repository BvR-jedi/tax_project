from datetime import time as dt_time

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Appointment


class AppointmentRequestForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'full_name',
            'email',
            'phone_number',
            'preferred_date',
            'preferred_time',
            'client_notes',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'type': 'time'}),
            'client_notes': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'full_name': 'Full name',
            'phone_number': 'Phone number',
            'preferred_date': 'Preferred date',
            'preferred_time': 'Preferred time',
            'client_notes': 'Notes for the accountant',
        }
        help_texts = {
            'preferred_date': 'Choose a date that is not in the past.',
            'preferred_time': 'Select a preferred time between 08:00 and 17:00.',
        }

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get('preferred_date')
        if preferred_date and preferred_date < timezone.localdate():
            raise ValidationError('Preferred date cannot be in the past.')
        return preferred_date

    def clean_preferred_time(self):
        preferred_time = self.cleaned_data.get('preferred_time')
        if preferred_time and (preferred_time < dt_time(8, 0) or preferred_time > dt_time(17, 0)):
            raise ValidationError('Please choose a time between 08:00 and 17:00.')
        return preferred_time
