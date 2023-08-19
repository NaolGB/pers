from .models import Departments, Profile, UserAccessLevel
from django.forms import ModelForm, fields


class DepartementsForm(ModelForm):
    class Meta:
        model = Departments
        fields = '__all__'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Exclude 'Superuser' access level from choices
        self.fields['access_level'].choices = [
            choice for choice in UserAccessLevel.choices if choice[0] != 'SU'
        ]

        # Exclude department named 'Superuser' from choices
        self.fields['department'].queryset = Departments.objects.exclude(name='Superuser')