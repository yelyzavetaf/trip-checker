from django.forms import HiddenInput
from tripchecker.ninjas_api import set_coordinates
from tripchecker.models import Trips
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TripsCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TripsCreateForm, self).__init__(*args, **kwargs)
        self.fields['latitude'].widget = HiddenInput()


    class Meta:
        model = Trips
        fields = ["name", "start", "end", "description", "latitude", "visited"]
        labels = {
            'name': 'City',
        }


        widgets = {
            'name': forms.TextInput(attrs={"placeholder": "City name"}),
            'start': forms.DateInput(attrs={'type': 'date'}),
            'end': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'cols': 10, 'rows': 3}),
            'visited': forms.RadioSelect()

        }

    def clean(self):
        super(TripsCreateForm, self).clean()
        coord = self.cleaned_data
        lat = coord['latitude']
        v = set_coordinates(str(coord['name']))
        if not v.latitude():
            self._errors['name'] = self.error_class([
                'That city is not found. Please check your spelling'])

        if coord['start'] > coord['end']:
            self._errors['start'] = self.error_class([
                'The dates are incorrect. Please check the start and the end of the trip'])
        return coord

class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']