from django import forms
from .models import IMSInventory

class AddInventoryForm(forms.ModelForm):
    class Meta:
        model = IMSInventory
        fields = '__all__'