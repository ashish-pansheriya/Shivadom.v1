# kundali/forms.py
from django import forms

class KundaliForm(forms.Form):
    name = forms.CharField(label='Full Name', max_length=100)
    birth_date = forms.DateField(label='Birth Date', widget=forms.DateInput(attrs={'type': 'date'}))
    birth_time = forms.TimeField(label='Birth Time', widget=forms.TimeInput(attrs={'type': 'time'}))
    latitude = forms.FloatField(label='Latitude')
    longitude = forms.FloatField(label='Longitude')
    timezone = forms.FloatField(label='Time Zone', initial=5.5)
