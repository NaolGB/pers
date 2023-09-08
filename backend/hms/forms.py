from django import forms
from .models import HMSProduct, HMSWarehouse, HMSStockTransaction

class ProductForm(forms.ModelForm):
    class Meta:
        model = HMSProduct
        fields = '__all__' 

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = HMSWarehouse
        fields = '__all__' 

class TransactionForm(forms.ModelForm):
    class Meta:
        model = HMSStockTransaction
        fields = ['product', 'quantity']