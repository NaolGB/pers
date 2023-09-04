from .models import Department, Profile, UserAccessLevel, UserRole
from django.forms import ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField


class DepartementsForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class ProfileForm(ModelForm):
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
        self.fields['department'].queryset = Department.objects.exclude(name='Superuser')

class ProfileFormEditProfile(ModelForm):
    class Meta:
        model = Profile
        fields = ['employee_id', 'department', 'access_level', 'user_roles']

    user_roles = ModelMultipleChoiceField(
        queryset=UserRole.objects.all(),
        widget=CheckboxSelectMultiple, 
    )
