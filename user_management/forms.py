from .models import Department, Profile, UserAccessLevel, UserRole
from django.forms import ModelForm, CheckboxSelectMultiple, ModelMultipleChoiceField


class DepartementsForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class ProfileFormEditProfile(ModelForm):
    class Meta:
        model = Profile
        fields = ['employee_id', 'department', 'access_level', 'user_roles']

    user_roles = ModelMultipleChoiceField(
        queryset=UserRole.objects.all(),
        widget=CheckboxSelectMultiple, 
    )
